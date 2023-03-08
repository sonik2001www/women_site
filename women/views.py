from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from random import randint
import re
from .models import *
from .form import *
from .utils import *


#############################################################################
#############################################################################
# def index(request):
#     posts = Women.objects.filter(is_published=True)
#
#     context = {
#         'posts': posts,
#         'title': 'головна сторінка',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenHome(DataMixin, ListView):
    # paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    # extra_context = {'title': 'Головна сторінка', 'cat_selected': 0}

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat_id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка',
                                      cat_selected=0)
        return dict(list(context.items()) + list(c_def.items()))


#############################################################################
#############################################################################


def about(request):
    return render(request, 'women/about.html')


#############################################################################
#############################################################################
# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             print(form.cleaned_data)
#             try:
#                 # Women.objects.create(**form.cleaned_data)
#                 form.save()
#                 return redirect('home')
#             except:
#                 form.add_error(None, 'Помилка добавлення поста')
#     else:
#         form = AddPostForm()
#     title = "Добавлення cтатті"
#     return render(request, 'women/addpage.html', locals())


# LoginRequiredMixin щоб керувати авторизованими користувачами
# а в функції використовується декоратор login_required


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # якщо немає абсолютної силки в моделях
    login_url = '/admin/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додавання статті')
        return dict(list(context.items()) + list(c_def.items()))


#############################################################################
#############################################################################


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Зворотній зв'язок")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # викликається якшо користувач ввів всі дані в форму вірно
        print(form.cleaned_data)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Сторінка не знайдена<h1/>")


#############################################################################
#############################################################################
# def show_post(request, post_slug):
#     post = Women.objects.get(slug=post_slug)
#
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id_id,
#     }
#     return render(request, 'women/post.html', context=context)


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # якшо по слагу
    # pk_url_kwarg = якшо по ід
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'],
                                      cat_selected=context['post'].cat_id_id)
        return dict(list(context.items()) + list(c_def.items()))


#############################################################################
#############################################################################


#############################################################################
#############################################################################
# def show_category(request, cat_slug):
#     cat = Category.objects.get(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat.id, is_published=True)
#
#     # if len(posts) == 0:
#     #     raise Http404()
#     print(posts)
#
#     context = {
#         'posts': posts,
#         'title': 'Відображення по рубрикам',
#         'cat_selected': cat.id,
#     }
#     return render(request, 'women/index.html', context=context)


class WomenCategory(DataMixin, ListView):
    # paginate_by = 3
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat_id__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat_id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категорія - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


#############################################################################
#############################################################################


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регістрація')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # викликається при успішній реєстрації
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def rooms(request):
    print(request.user)
    user = str(request.user)
    rooms = GameRoom.objects.filter(attempt_2=0) | GameRoom.objects.filter(attempt_1=0)
    rooms_user = GameRoom.objects.filter(user_2=user) | GameRoom.objects.filter(user_1=user)
    return render(request, 'women/rooms.html', locals())


def game(request, pk):
    room = GameRoom.objects.get(pk=pk)
    form = GameForm()

    if str(request.user) != room.user_1:
        room.user_2 = str(request.user)
        if request.method == 'GET':
            form = GameForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data)
                if form.cleaned_data['year_1'] == room.year_1:
                    room.score_2 += 1
                if form.cleaned_data['year_2'] == room.year_2:
                    room.score_2 += 1
                if form.cleaned_data['year_3'] == room.year_3:
                    room.score_2 += 1
                room.attempt_2 = 1

                if room.attempt_1 > 0 and room.attempt_2 > 0:
                    if room.score_1 > room.score_2:
                        room.winner = 'перемога ' + room.user_1
                    elif room.score_1 < room.score_2:
                        room.winner = 'перемога ' + room.user_2
                    else:
                        room.winner = 'нічія'
                room.save()

                return redirect('rooms')

    if str(request.user) == room.user_1:
        if request.method == 'GET':
            form = GameForm(request.GET)
            if form.is_valid():
                print(form.cleaned_data)
                # room.score_1 = 0
                if form.cleaned_data['year_1'] == room.year_1:
                    room.score_1 += 1
                if form.cleaned_data['year_2'] == room.year_2:
                    room.score_1 += 1
                if form.cleaned_data['year_3'] == room.year_3:
                    room.score_1 += 1
                room.attempt_1 = 1

                if room.attempt_1 > 0 and room.attempt_2 > 0:
                    if room.score_1 > room.score_2:
                        room.winner = 'перемога ' + room.user_1
                    elif room.score_1 < room.score_2:
                        room.winner = 'перемога ' + room.user_2
                    else:
                        room.winner = 'нічія'
                room.save()

                return redirect('rooms')

    return render(request, 'women/game.html', locals())


def start_game(request):
    user = str(request.user)
    womens = Women.objects.filter(is_published=True)
    names_years = []

    tmp = []
    while len(tmp) < 3:
        x = randint(0, len(womens)-1)
        if x not in tmp:
            tmp.append(x)

    for j in tmp:

        regex_num = re.compile('\d+')
        a = regex_num.findall(womens[j].content)

        for i in a:
            if len(i) == 4:
                names_years.append(i)
                break
        names_years.append(womens[j].title)

    room = GameRoom(user_1=user,
                    name_1=names_years[1],
                    name_2=names_years[3],
                    name_3=names_years[5],
                    year_1=names_years[0],
                    year_2=names_years[2],
                    year_3=names_years[4])
    room.save()

    return redirect('rooms')


def chat_rooms(request):
    users = User.objects.all()
    main_user = str(request.user)
    rooms = Chat.objects.filter(user_1=main_user) | Chat.objects.filter(user_2=main_user)

    users = [u.username for u in users]

    for r in rooms:
        try:
            users.remove(r.user_1)
        except ValueError:
            pass
        try:
            users.remove(r.user_2)
        except ValueError:
            pass

    if request.method == 'POST':
        user_2 = request.POST.get('user_2')
        room = Chat(user_1=main_user,
                    user_2=str(user_2))
        room.save()
        return redirect(f'/chat/{room.pk}')

    return render(request, 'women/chat_rooms.html', locals())


def chat(request, pk):
    room = Chat.objects.get(pk=pk)
    main_user = str(request.user)

    if request.method == 'POST':
        message = '&&&' + request.POST.get('message')
        user_8 = '&&&' + str(request.user) + '&&&'
        message += user_8

        room.content += message
        room.save()
        room.content += str(room.time_update)[:19]
        room.save()

    content = room.content
    content = content.split("&&&")
    content.remove('')
    content = [content[i:i+3] for i in range(0, len(content), 3)]
    print(content, type(content))
    content_paginator = Paginator(content[::-1], 4)

    page_number = request.GET.get('page')
    page_obj = content_paginator.get_page(page_number)

    return render(request, 'women/chat.html', locals())

