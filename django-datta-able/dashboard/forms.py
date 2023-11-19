# Dans forms.py

from django import forms
from .models import CoachTable, TeamTable

class CoachCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CoachTable
        fields = ['email', 'username', 'password']

class TeamCreationForm(forms.ModelForm):
    class Meta:
        model = TeamTable
        fields = ['teamName', 'teamGitlabAccessToken']
