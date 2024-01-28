from django.contrib import admin
from django.urls import path
from .views import base_part, chat_bot, data_search

urlpatterns = [
    path('', base_part, name='base-part'),
    path('chat/', chat_bot, name='chat-bot'),
    path('search/', data_search, name='data-search')
]
