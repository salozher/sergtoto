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
    bets_winners,
    contest_participants,
    add_participant_to_contest,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', home_view, name='home'),
    path('team/<str:slug>/', team_view, name='team_detail'),
    path('makebet/<int:pk>/', make_bet, name='make_bet'),
    path('betswinners/<str:slug>/', bets_winners, name='bets_winners'),

    path('contest/upload/', AddNewContestView.as_view(), name='add_new_contest'),
    path('contest/participants/<str:slug>/', contest_participants, name='contest_participants'),
    path('contest/add_participant_to_contest/<str:contest_slug>/<str:team_slug>/', add_participant_to_contest,
         name='add_participant'),

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
