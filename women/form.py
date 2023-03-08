from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


# class AddPostForm(forms.Form):
    # title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label='URL')
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Опис')
    # # photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    # is_published = forms.BooleanField(label='Публікація', required=False, initial=True)
    # cat_id = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категорія', empty_label='категорія не вибрана')

class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat_id'].empty_label = 'категорія не вибрана'

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat_id']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self): #валідатор
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Довжина не може мати більше ніж 200 символів')
        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Лоін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Лоін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='імя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class GameForm(forms.Form):
    year_1 = forms.IntegerField()
    year_2 = forms.IntegerField()
    year_3 = forms.IntegerField()