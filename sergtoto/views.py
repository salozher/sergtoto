from datetime import date

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import AddNewTeamForm, AddNewBetForm, AddNewContestForm, AddNewGameForm
from .models import MyUser, Team, Game, Contest, Bet


def home_view(request):
    contests = Contest.objects.all()
    games = Game.objects.all()
    context = {
        'contests': contests,
        "games": games,
    }
    # returns render(request, template of certain product or element, context dictionary)
    return render(request, 'home.html', context)


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
    games = contest.game.objects.all()
    complete_games = games.filter(game_is_played=True)
    context = {
        'contest': contest,
        'games': games,
    }
    return render(request, 'contestgames.html', context)


class AddNewTeamView(CreateView):
    model = Team
    form_class = AddNewTeamForm
    success_url = reverse_lazy('my_teams')
    template_name = 'add_new_team.html'

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super(AddNewTeamView, self).form_valid(form)


class AddNewBetView(CreateView):
    model = Bet
    form_class = AddNewBetForm
    success_url = reverse_lazy('bets_history')
    template_name = 'add_new_bet.html'

    def form_valid(self, form):
        form.instance.user_id = self.request.user.id
        return super(AddNewBetView, self).form_valid(form)


class AddNewContestView(CreateView):
    model = Contest
    form_class = AddNewContestForm
    success_url = reverse_lazy('home')
    template_name = 'add_new_contest.html'

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


def delete_team(request, pk):
    if request.method == 'POST':
        team = Team.objects.get(pk=pk)
        team.delete()
    return redirect('my_teams')


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
