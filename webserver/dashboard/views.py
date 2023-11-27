import datetime
from django.http import HttpRequest, HttpResponse
from .models import GitlabAccessRepo, TeamMood, Utilisateur

from.serializers import MoodSerializer
from .forms import GitlabAccessRepoForm, RegisterForm, TeamTableForm 
from django.shortcuts import redirect, render
from django.contrib.auth import login , logout , authenticate 
from django.contrib.auth.decorators import login_required , user_passes_test
# Create your views here.

from utils import gitAPI
from rest_framework.views import APIView
from rest_framework.response import Response

import utils.gitAPI as gitAPI

@user_passes_test(lambda u: u.is_authenticated or u.is_superuser, login_url="/login")
def home(request : HttpRequest):
    print(request.user.id )
    return render(request , 'dashboard/index.html')

@login_required(login_url="/login")
def addTeam(request):
    if request.method == 'POST':
        form = TeamTableForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            # Set additional fields if needed
            team.save()
            return redirect('dashboard:home')  # Redirect to the appropriate page after saving
    else:
        # Set the initial data for the form
        initial_data = {'coachs': [request.user.id]}
        form = TeamTableForm(initial=initial_data)

    return render(request, 'dashboard/add_team.html', {'form': form})


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user )
            return redirect("/dashboard")

    else:
        form = RegisterForm()
    
    return render(request , "registration/signup.html" , {"form" :  form })


@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # Redirect to the user list page or any other page
    else:
        form = RegisterForm()

    return render(request, 'registration/create_user.html', {'form': form})


class MoodView(APIView):
    def post(self, request, format=None):
        serializer = MoodSerializer(data=request.data)

        if serializer.is_valid():
            # Valid data
            moodLevel = serializer.validated_data['moodLevel']
            message = serializer.validated_data['message']
            email = serializer.validated_data['email']

            user = Utilisateur.objects.filter(email=email).first()

            team = user.teams.all()

            mood = TeamMood.objects.create(timeStamp=datetime.now(), moodLevel=moodLevel, message=message)
            mood.teams.set(team)

            return Response({'status': 'success',
                            'message': 'Data received and processed successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@require_http_methods(["GET", "POST"])

@login_required(login_url="/login")
def addNewToken(request):
    if request.method == 'GET':
        # Si la méthode est GET, renvoyer le formulaire
        form = GitlabAccessRepoForm()
        return render(request, "dashboard/token_form.html", {'form': form})

    elif request.method == 'POST':
        # Si la méthode est POST, valider le formulaire
        form = GitlabAccessRepoForm(request.POST)

        if form.is_valid():
            # Si le formulaire est valide, enregistrer les données dans le modèle
            gitlab_access_repo = GitlabAccessRepo(
                token=form.cleaned_data['gitlab_token'],
                url=form.cleaned_data['server_url'],
                projectName=form.cleaned_data['project_name']
            )
            gitlab_access_repo.save()

            res = gitAPI.list_projects_users(form.cleaned_data['server_url'] , form.cleaned_data['gitlab_token']) 


            

            # Vous pouvez également appeler la fonction gitAPI.list_projects_users ici si nécessaire

            # Retourner une réponse, vous pouvez également rediriger vers une autre vue ou un template
            return HttpResponse("Le token a été ajouté avec succès.")
        else:
            # Si le formulaire n'est pas valide, le renvoyer avec les erreurs
            return render(request, "dashboard/token_form.html", {'form': form})
