from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib import admin
from .views import (
    home_view,
    team_view,
    teams_view,
    my_teams_view,
    bets_history,
    contest_games_view,
    AddNewTeamView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # path('contest/<str:slug>/', contest_games_view(), name='contest_detail'),
    path('team/<str:slug>/', team_view, name='team_detail'),

    path('teams/upload/', AddNewTeamView.as_view(), name='add_new_team'),
    path('showmyteams/', my_teams_view, name='my_teams'),
    path('showteams/', teams_view, name='show_teams'),
    path('betshistory/', bets_history, name='bets_history'),

    path('', home_view, name='home')
]
