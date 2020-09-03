from django import forms

from .models import Team


class AddNewTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'description')

    def __init__(self, *args, **kwargs):
        super(AddNewTeamForm, self).__init__(*args, **kwargs)