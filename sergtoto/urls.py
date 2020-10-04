from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from .views import (
    home_view,
    team_view,
    teams_view,
    my_teams_view,
    bets_history,
    contest_games_view,
    AddNewTeamView,
    AddNewBetView,
    my_bets_history,
    AddNewContestView,
    AddNewGameView,
    make_bet,
    game_view,
    generate_tournament,
    too_many_teams_view,
    generate_teams,
    update_game,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', home_view, name='home'),
    # path('contest/<str:slug>/', contest_games_view(), name='contest_detail'),
    path('team/<str:slug>/', team_view, name='team_detail'),
    path('makebet/<int:pk>/', make_bet, name='make_bet'),
    path('contest/upload/', AddNewContestView.as_view(), name='add_new_contest'),
    path('game/upload/', AddNewGameView.as_view(), name='add_new_game'),
    path('game/update/<str:slug>/', update_game, name='update_game'),

    path('teams/upload/', AddNewTeamView.as_view(), name='add_new_team'),
    path('bets/upload/', AddNewBetView.as_view(), name='add_new_bet'),

    path('games/<str:slug>/', generate_tournament, name='games'),
    path('generateteams/', generate_teams, name='generate_teams'),

    path('game/<int:pk>/', game_view, name='game'),

    path('contestgames/<str:slug>/', contest_games_view, name='contest_games'),

    path('showmyteams/', my_teams_view, name='my_teams'),
    path('showteams/', teams_view, name='show_teams'),
    path('betshistory/', bets_history, name='bets_history'),
    path('mybetshistory/', my_bets_history, name='my_bets_history'),
    path('toomanyteamswarning/', too_many_teams_view, name='too_many_teams_warning'),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
