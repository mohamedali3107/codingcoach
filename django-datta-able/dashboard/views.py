from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CoachCreationForm, TeamCreationForm
# Create your views here.

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
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

from django.shortcuts import render

def signup(request):
    # Votre logique de vue ici
    return render(request, 'signup.html')  # Assurez-vous d'avoir le template signup.html dans le dossier templates
