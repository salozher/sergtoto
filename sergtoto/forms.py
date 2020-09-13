from django import forms
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
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


class AddNewContestForm(forms.ModelForm):
    contest_date = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = Contest
        fields = ('contest_date',)

    def __init__(self, *args, **kwargs):
        super(AddNewContestForm, self).__init__(*args, **kwargs)


class AddNewGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('contest', 'team_a', 'team_b', 'game_time')

    def __init__(self, *args, **kwargs):
        super(AddNewGameForm, self).__init__(*args, **kwargs)

