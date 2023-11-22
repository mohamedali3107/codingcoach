from django.shortcuts import render
from django.contrib.auth import authenticate

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .forms import CoachCreationForm, LoginForm, SignUpForm, TeamCreationForm
from .models import CoachTable, TeamMood
# Create your views here.

app_name = "dashboard"


def index(request):

#   context = {
#     'segment'  : 'index',
#     #'products' : Product.objects.all()
#   }
  return render(request, "dashboard/index.html")


# Dans views.py

@login_required
def create_coach(request):
    if request.method == 'POST':
        form = CoachCreationForm(request.POST)
        if form.is_valid():
            coach = form.save()
            # Faire quelque chose avec le coach créé (redirection, affichage, etc.)
            return redirect('index')
    else:
        form = CoachCreationForm()
    return render(request, 'create_coach.html', {'form': form})

@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamCreationForm(request.POST)
        if form.is_valid():
            team = form.save()
            # Faire quelque chose avec la team créée (redirection, affichage, etc.)
            return redirect('index')
    else:
        form = TeamCreationForm()
    return render(request, 'create_team.html', {'form': form})


# Dans views.py


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if passwords match
            if password == confirm_password:
                # Create a new user
                user = CoachTable.objects.create_user(email=email, username=username, password=password)
                
                # Log in the user
                login(request, user)

                # Redirect the user to the desired page (e.g., dashboard:index)
                return redirect('dashboard:index')
            else:
                # Passwords don't match, handle the error (e.g., add an error message to the form)
                pass
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect the user to the desired page (e.g., dashboard:index)
                return redirect('dashboard:index')
            else:
                # Handle invalid login credentials
                # You might want to add an error message to the form or handle it in another way
                pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
