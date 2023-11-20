from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .forms import CoachCreationForm, SignUpForm, TeamCreationForm
# Create your views here.

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "dashboard/index.html")


# Dans views.py


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
            # Enregistrez l'utilisateur dans la base de données
            user = form.save()
            # Connectez automatiquement l'utilisateur après l'inscription
            login(request, user)
            # Redirigez l'utilisateur vers la page de succès ou toute autre page souhaitée
            return redirect('dashboard:index')  # Remplacez 'success' par le nom de votre page de succès
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})