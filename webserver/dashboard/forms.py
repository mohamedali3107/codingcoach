# Dans forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User

from dashboard.models import TeamTable 

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
    email = forms.EmailField(required=True)
    class Meta:
        model = User 
        fields = ['username', "email" ,'password1' , "password2"]


class TeamTableForm(forms.ModelForm):
    coachs = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = TeamTable
        fields = ['teamName', 'teamGitlabAccessToken', 'coachs']