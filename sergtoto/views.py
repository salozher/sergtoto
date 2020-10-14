# from datetime import datetime
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from itertools import combinations

from .forms import AddNewTeamForm, AddNewBetForm, AddNewContestForm, AddNewGameForm, SelectTeamForm, ChangeGameForm, \
    AddNewParticipantForm
from .models import MyUser, Team, Game, Contest, Bet, ParticipantTeam


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
    if not contest.games_sheduled:
        contest.games_sheduled = True

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
    contest.save()
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
    contests = Contest.objects.filter(games_sheduled=False)

    context = {
        'my_teams': my_teams,
        'contests': contests,
    }
    return render(request, 'my_teams.html', context)


def add_participant_to_contest(request, contest_slug, team_slug):
    contest = Contest.objects.get(slug=contest_slug)
    team = Team.objects.get(slug=team_slug)
    participants = ParticipantTeam.objects.filter(contest=contest)
    participant = ParticipantTeam()
    participant.contest = contest
    participant.team = team
    no_duplicats = True
    message = ''

    message1 = 'Cannot add this team to the contest. The maximum teams amount for this contest is reached.'
    message0 = 'This Team is already added to this Contest'

    context1 = {
        'message': message1,
    }
    context0 = {
        'message': message0,
    }
    if len(participants) == 0:
        participant.save()
        participants = ParticipantTeam.objects.filter(contest=contest)
        context = {
            'contest': contest,
            'participants': participants,
        }
        return render(request, 'contest_participants.html', context)

    if (len(participants) < contest.max_teams) and participants:
        for member in participants:
            if member.team == team:
                no_duplicats = False
        if no_duplicats:
            participant.save()
            participants = ParticipantTeam.objects.filter(contest=contest)
            context = {
                'contest': contest,
                'participants': participants,
            }
            return render(request, 'contest_participants.html', context)
        else:
            message = message1
            return render(request, 'warning_message.html', context0)
    else:
        message = message0
        return render(request, 'warning_message.html', context1)


def contest_participants(request, slug):
    # contest = Contest.objects.get(slug=slug)
    participants = ParticipantTeam.objects.filter(contest__slug=slug)

    context = {
        'participants': participants,
    }
    return render(request, 'contest_participants.html', context)


def team_view(request, slug):
    team = Team.objects.get(slug=slug)
    context = {
        'team': team,
    }
    return render(request, 'team.html', context)


def teams_for_contest(request, pk):
    if request.method == 'POST':
        team = Team.objects.get(pk=pk)
        form = AddNewBetForm(request.POST)
        checked_radiobuttons = request.POST.getlist('checks[]')
        winner = checked_radiobuttons[0]
        form.instance = request.user.id
        if winner == '1':
            form.instance.team_a_win = True
        elif winner == '2':
            form.instance.team_b_win = True
        elif winner == '3':
            form.instance.draw = True
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('betshistory')


def contest_games_view(request, slug):
    contest = Contest.objects.get(slug=slug)
    games = Game.objects.filter(contest=contest.id)
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


class ChangeTeamView(CreateView):
    model = Team
    form_class = AddNewTeamForm
    success_url = reverse_lazy('my_teams')
    template_name = 'my_teams.html'

    def form_valid(self, form):
        selectedteams = Team.objects.filter(selected_for_contest=True)
        if selectedteams.count() < 101:
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
    return render(request, 'warning_message.html', context)


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


def update_game(request, slug):
    if request.method == 'POST':
        game = Game.objects.get(slug=slug)
        # create a form instance and populate it with data from the request:
        form = ChangeGameForm(request.POST)
        if form.is_valid():
            game_is_started = form.cleaned_data['game_is_started']
            game_is_played = form.cleaned_data['game_is_played']
            score_team_a = form.cleaned_data['score_team_a']
            score_team_b = form.cleaned_data['score_team_b']
            if score_team_a > 0 or score_team_b > 0:
                game_is_started = True

            game.game_is_started = game_is_started
            game.game_is_played = game_is_played
            game.score_team_a = score_team_a
            game.score_team_b = score_team_b

            game.save()
        return redirect('home')
    else:
        game = Game.objects.get(slug=slug)
        form = ChangeGameForm(instance=game)
        context = {
            'form': form,
        }
        return render(request, 'add_new_games.html', context)
        # return redirect('bets_history')


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
    games = Game.objects.filter(game_is_played=True)
    for game in games:
        for bet in bets:
            if bet.game == game:
                if (game.score_team_a > game.score_team_b) and bet.team_a_win:
                    bet.bet_won = True
                if (game.score_team_b > game.score_team_a) and bet.team_b_win:
                    bet.bet_won = True
                if (game.score_team_b == game.score_team_a) and bet.draw:
                    bet.bet_won = True
            bet.save()

    context = {
        'bets': bets,
        'games': games,
    }
    return render(request, 'bets_history.html', context)


def bets_winners(request, slug):
    game = Game.objects.get(slug=slug)
    bets = Bet.objects.filter(bet_won=True, game=game)

    context = {
        'bets': bets,
        'game': game,
    }
    return render(request, 'bets_winners.html', context)


def my_bets_history(request):
    request = request
    current_user = MyUser.objects.get(username=request.user.username)
    bets = Bet.objects.filter(user=current_user)
    games = Game.objects.filter(game_is_played=True)
    for game in games:
        for bet in bets:
            if bet.game == game:
                if (game.score_team_a > game.score_team_b) and bet.team_a_win:
                    bet.bet_won = True
                if (game.score_team_b > game.score_team_a) and bet.team_b_win:
                    bet.bet_won = True
                if (game.score_team_b == game.score_team_a) and bet.draw:
                    bet.bet_won = True
            bet.save()

    context = {
        'bets': bets,
        'games': games,
    }
    return render(request, 'bets_history.html', context)
