from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Team, Bet, Contest, Game


class AddNewTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(AddNewTeamForm, self).__init__(*args, **kwargs)


class AddNewBetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('amount',)

    def __init__(self, *args, **kwargs):
        super(AddNewBetForm, self).__init__(*args, **kwargs)


class ChangeGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_is_started', 'score_team_a', 'score_team_b', 'game_is_played',)

    def __init__(self, *args, **kwargs):
        super(ChangeGameForm, self).__init__(*args, **kwargs)


class AddNewContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ('contest_start_date', 'game_length', 'pause_length')

    def __init__(self, *args, **kwargs):
        super(AddNewContestForm, self).__init__(*args, **kwargs)


class AddNewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('game_is_started', 'score_team_a', 'score_team_b', 'game_is_played')

    def __init__(self, *args, **kwargs):
        super(AddNewGameForm, self).__init__(*args, **kwargs)


class DateForm(forms.ModelForm):
    # date = forms.DateTimeField(
    #     input_formats=['%d/%m/%Y %H:%M'],
    #     widget=forms.DateTimeInput(attrs={
    #         'class': 'form-control datetimepicker-input',
    #         'data-target': '#datetimepicker1'
    #     })
    # )

    class Meta:
        model = Contest
        fields = ('contest_start_date', 'game_length', 'pause_length')

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
