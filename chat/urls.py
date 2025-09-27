from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('start/<int:room_id>/', views.start_chat_with_owner, name='start_chat'),
    path('room/<int:chat_room_id>/', views.chat_room, name='chat_room'),
    path('send-message/', views.send_message, name='send_message'),
    path('messages/<int:chat_room_id>/', views.get_chat_messages, name='get_messages'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
    path('debug/', views.debug_chat, name='debug'),  # Debug page
]