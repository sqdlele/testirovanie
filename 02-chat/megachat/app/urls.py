from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_room, name='create_room'),
    path('room/<slug:slug>/', views.room, name='room'),
    path('delete/<slug:slug>/', views.delete_room, name='delete_room'),
    path('api/messages/<slug:slug>/', views.get_messages, name='get_messages'),
    path('api/send-message/', views.send_message, name='send_message'),
]
