from django.urls import path, include
from django.views.decorators.cache import cache_page
from .views import *


urlpatterns = [
    # path('', index, name='home'),
    # path('', cache_page(60)(WomenHome.as_view()), name='home'),
    # приклад кешування сторінки
    path('', WomenHome.as_view(), name='home'),
    path('about/', about, name='about'),
    path('rooms/', rooms, name='rooms'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),
    path('register', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('game/<int:pk>', game, name='game'),
    path('game/', start_game, name='start_game'),
    path('chat/', chat_rooms, name='chat_rooms'),
    path('chat/<int:pk>', chat, name='chat'),

]