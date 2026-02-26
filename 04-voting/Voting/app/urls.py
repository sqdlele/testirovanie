from django.urls import path
from . import views

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('poll/create/', views.poll_create, name='poll_create'),
    path('poll/<int:pk>/', views.poll_detail, name='poll_detail'),
    path('poll/<int:pk>/vote/', views.poll_vote, name='poll_vote'),
    path('poll/<int:pk>/comment/', views.poll_comment, name='poll_comment'),
    path('poll/<int:pk>/results/', views.poll_results, name='poll_results'),
]
