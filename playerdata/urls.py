from django.urls import path
from . import views

urlpatterns = [
    path('player/<int:player_id>/', views.player_detail, name='player_detail'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('matches/', views.match_list, name='match_list'),
    path('players/', views.player_list, name='player_list'),
    path('teams/', views.team_list, name='team_list'),
    path('champ_stats/', views.champ_stats, name='champ_stats'),
    path('role_stats/<int:role_id>/', views.role_stats, name='role_stats'),
    path('', views.home, name='home'),
]
