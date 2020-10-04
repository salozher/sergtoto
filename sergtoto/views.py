# from datetime import datetime
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from itertools import combinations

from .forms import AddNewTeamForm, AddNewBetForm, AddNewContestForm, AddNewGameForm, DateForm
from .models import MyUser, Team, Game, Contest, Bet


# here you can make your bet
def game_view(request, pk):
    if request.method == 'POST':
        game = Game.objects.get(pk=pk)
        # create a form instance and populate it with data from the request:
        form = AddNewBetForm(request.POST)
        # form.instance.amount =
        checked_radiobuttons = request.POST.getlist('checks[]')
        winner = checked_radiobuttons[0]
        form.instance.user = request.user
        form.instance.game = game
        if winner == '1':
            form.instance.team_a_win = True
        elif winner == '2':
            form.instance.team_b_win = True
        elif winner == '3':
            form.instance.draw = True
        if form.is_valid():
            form.save()
        return redirect('my_bets_history')
    else:
        game = Game.objects.get(pk=pk)
        form = AddNewBetForm()
        contests = Contest.objects.all
        games = Game.objects.filter(pk=game.pk)
        checked_radiobuttons = request.POST.getlist('checks')
        context = {
            'form': form,
            'contests': contests,
            'games': games,
            'checked_radiobuttons': checked_radiobuttons,
        }
        return render(request, 'game_bet.html', context)
        # return redirect('bets_history')


def home_view(request):
    contests = Contest.objects.all()
    games = Game.objects.all()

    context = {
        'contests': contests,
        'games': games,
    }
    return render(request, 'home.html', context)


def generate_teams(request):
    totalTeams = 100
    for i in range(totalTeams):
        newteam = Team()
        newteam.name = i
        newteam.description = i
        newteam.added_by = request.user
        newteam.save()
    return redirect('home')


def generate_tournament(request, slug):
    contest = Contest.objects.get(slug=slug)
    existinggames = Game.objects.filter(contest=contest)
    if existinggames.count() < 1:

        contest = Contest.objects.get(slug=slug)
        teams = Team.objects.all()
        teamsidlist = []
        for team in teams:
            teamsidlist.append(team.id)

        games = list(combinations(teamsidlist, 2))
        workedoutgames = []
        gamestarttime = contest.contest_start_date

        while games:
            game = games.pop(0)
            currentexistinggames = Game.objects.filter(contest=contest, game_date_time=gamestarttime)
            newgame = Game()
            newgame.team_a = Team.objects.get(id=int(game[0]))
            newgame.team_b = Team.objects.get(id=int(game[1]))
            newgame.contest = contest
            newgame.game_date_time = gamestarttime

            if currentexistinggames:
                duplicateexist = False
                # currentexistinggames = Game.objects.filter(contest=contest, game_date_time=gamestarttime)
                for oneofgames in currentexistinggames:
                    if oneofgames.team_a.id == newgame.team_a.id or oneofgames.team_a.id == newgame.team_b.id or oneofgames.team_b.id == newgame.team_a.id or oneofgames.team_b.id == newgame.team_b.id:
                        duplicateexist = True

                if not duplicateexist:
                    newgame.save()
                else:
                    workedoutgames.append(game)
            if currentexistinggames.count() == 0:
                newgame.save()
            if not games:
                games = workedoutgames.copy()
                workedoutgames.clear()
                minutesadded = datetime.timedelta(minutes=contest.game_length + contest.pause_length)
                gamestarttime = gamestarttime + minutesadded

    return redirect('home')


def make_bet(request, pk):
    if request.method == 'POST':
        game = Game.objects.get(pk=pk)
        form = AddNewBetForm(request.POST)
        checked_radiobuttons = request.POST.getlist('checks[]')
        winner = checked_radiobuttons[0]
        form.instance = request.user.id
        form.instance.game_id = game.id
        if winner == '1':
            form.instance.team_a_win = True
        elif winner == '2':
            form.instance.team_b_win = True
        elif winner == '3':
            form.instance.draw = True
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('betshistory')


def teams_view(request):
    teams = Team.objects.all()
    context = {
        'teams': teams,
    }
    return render(request, 'show_teams.html', context)


def my_teams_view(request):
    current_user = MyUser.objects.get(username=request.user.username)
    my_teams = Team.objects.filter(added_by=current_user)

    context = {
        'my_teams': my_teams,
    }
    return render(request, 'my_teams.html', context)


def team_view(request, slug):
    team = Team.objects.get(slug=slug)
    context = {
        'team': team,
    }
    return render(request, 'team.html', context)


def contest_games_view(request, slug):
    contest = Contest.objects.get(slug=slug)
    games = Game.objects.filter(contest=contest.id, game_is_started=False, game_is_played=False)
    complete_games = games.filter(game_is_played=True)
    context = {
        'contest': contest,
        'games': games,
    }
    return render(request, 'contest_games.html', context)


class AddNewTeamView(CreateView):
    model = Team
    form_class = AddNewTeamForm
    success_url = reverse_lazy('my_teams')
    template_name = 'add_new_team.html'

    def form_valid(self, form):
        existingteams = Team.objects.all()
        if existingteams.count() < 100:
            form.instance.added_by = self.request.user
            return super(AddNewTeamView, self).form_valid(form)
        else:
            return redirect('too_many_teams_warning')


def delete_team(request, pk):
    if request.method == 'POST':
        team = Team.objects.get(pk=pk)
        team.delete()
    return redirect('my_teams')


def too_many_teams_view(request):
    teams = Team.objects.all()
    context = {
        'teams': teams,
    }
    return render(request, 'too_many_teams.html', context)


class AddNewBetView(CreateView):
    model = Bet
    form_class = AddNewBetForm
    success_url = reverse_lazy('bets_history')
    template_name = 'add_new_bet.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        form.instance.team_a_win = True
        return super(AddNewBetView, self).form_valid(form)


class AddNewContestView(CreateView):
    model = Contest
    form_class = AddNewContestForm
    success_url = reverse_lazy('home')
    template_name = 'new_contest.html'

    def form_valid(self, form):
        # form.instance.user_id = self.request.user.id
        return super(AddNewContestView, self).form_valid(form)


class AddNewGameView(CreateView):
    model = Game
    form_class = AddNewGameForm
    success_url = reverse_lazy('home')
    template_name = 'add_new_games.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(AddNewGameView, self).form_valid(form)


def bets_history(request):
    request = request
    current_user = MyUser.objects.get(username=request.user.username)
    # bets = Bet.objects.filter(user=current_user)
    bets = Bet.objects.all()
    context = {
        'bets': bets,
    }
    return render(request, 'bets_history.html', context)


def my_bets_history(request):
    request = request
    current_user = MyUser.objects.get(username=request.user.username)
    bets = Bet.objects.filter(user=current_user)
    # bets = Bet.objects.all()
    context = {
        'bets': bets,
    }
    return render(request, 'bets_history.html', context)
