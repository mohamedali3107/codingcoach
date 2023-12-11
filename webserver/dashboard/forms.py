from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from .models import Coach, TeamTable, GitlabAccessRepo

# class CoachCreationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = CoachTable
#         fields = ['email', 'username', 'password']

# class TeamCreationForm(forms.ModelForm):
#     class Meta:
#         model = TeamTable
#         fields = ['teamName', 'teamGitlabAccessToken']



class RegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)
    class Meta:
        model = Coach 
        fields = [ "username"  ,'password1' , "password2"]


class TeamTableForm(forms.ModelForm):
    coachs = forms.ModelMultipleChoiceField(queryset=Coach.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = TeamTable
        fields = ['teamName', 'repos', 'coachs']

class GitlabAccessRepoForm(forms.ModelForm):
    class Meta:
        model = GitlabAccessRepo
        fields = ['url', 'token', 'projectName']
