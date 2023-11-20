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



class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    # Ajoutez d'autres champs si nécessaire
    class Meta:
        model = CoachTable
        fields = ['email', 'username', 'password']
