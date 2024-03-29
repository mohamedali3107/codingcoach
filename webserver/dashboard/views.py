import datetime
from django.http import HttpRequest, HttpResponse
from .models import Coach, CoachCas, GitlabAccessRepo, TeamMood, TeamRepo, TeamTable, Utilisateur
from django.contrib.auth.models import User, BaseUserManager

from.serializers import MoodSerializer
from .forms import GitlabAccessRepoForm, RegisterForm, TeamTableForm 
from django.shortcuts import redirect, render
from django.contrib.auth import login , logout , authenticate 
from django.contrib.auth.decorators import login_required , user_passes_test
from rest_framework import status
# Create your views here.

from utils import gitAPI
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import utils.gitAPI as gitAPI
import random

def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return wrapper



@user_passes_test(lambda u: u.is_authenticated or u.is_superuser, login_url="/login")
def home(request):
    user = request.user
    
    # Try to retrieve CoachCas instance for the authenticated CAS user
    coach = None 
    try: 
        coach = CoachCas.objects.get(user=user) 
    except:
        coach = CoachCas.objects.create(user=user)




    print("COACH " , coach)

    print(coach.user)
    print(coach.teams)


    # Retrieve all teams managed by the coach
    teams_managed_by_coach = coach.teams.all()
    print(teams_managed_by_coach)
    # Create dictionaries to store users, moods, and repos for each team
    team_data = {}
    gitlab_access_repo_info = {}

   
    for team in teams_managed_by_coach:
        print("TEAM " , team ) 

        # Retrieve users, moods, and repos for each team
        users = team.users.all()
        moods = team.moods.all()
        repos = team.repos.all()
        if repos:
            last_repo = repos.latest('timeStamp')
        else:
            last_repo = repos
        
        # Retrieve GitLab information using the stored GitLab access token and repository URL
        gitlab_repo = team.gitlabRepo

        # Retrieve information from the GitlabAccessRepo model
        gitlab_access_repo_info = {
            'token': gitlab_repo.token,
            'url': gitlab_repo.url,
            'projectName': gitlab_repo.projectName,
        }
        
        average_mood = 0
        n = 0
        for user in users:
            n += 1
        i=0
        if moods.exists() and users.exists():
            day = moods[0].timeStamp.day
            for mood in moods:
                if mood.timeStamp.day == day:
                    average_mood += mood.moodLevel
                    if i == n:
                        break
                    i += 1
            average_mood = average_mood/n
        else:
            average_mood = -1
            
        team_data[team] = {
            'users': users,
            'mood': average_mood,
            'repo': last_repo,
            'gitlab_access_repo_info': gitlab_access_repo_info,
        }
    
    data = {}
    data['team_data'] = team_data
    data['coach_data'] = {'user': coach.user.username}    

    return render(request, 'dashboard/index.html', {'data': data})



@login_required(login_url="/login")
def update_repo(request):
    print("------------UPDATE REPO---------------")
    # Assuming the logged-in user is a coach
    user = request.user
    coach = CoachCas.objects.get(user=user)

    # Retrieve all teams managed by the coach
    teams_managed_by_coach = coach.teams.all()

    print("TEAMS UNDER SUPERVISION : " , teams_managed_by_coach)

    for team in teams_managed_by_coach:
        # Retrieve GitLab information using the stored GitLab access token and repository URL
        gitlab_repo = team.gitlabRepo

        # Retrieve information from the GitlabAccessRepo model
        gitlab_access_repo_info = {
            'token': gitlab_repo.token,
            'url': gitlab_repo.url,
            'projectName': gitlab_repo.projectName,
        }

        # Compute information using the gitAPI.compute_all function
        computed_info = gitAPI.compute_all(
            gitlab_access_repo_info['url'],
            gitlab_access_repo_info['token'],
            gitlab_access_repo_info['projectName']
        )

        print("-----------------------------------------")
        #print(computed_info)

        # Create an instance of TeamRepo and save the computed information
        team_repo = TeamRepo(
            branchNumber=computed_info['get_branch_number'],
            branchBehindMax=computed_info['most_behind_branch'],
            branchAheadMax=computed_info['most_ahead_branch'],
            lastPrTime=computed_info['last_PR_time'],
            commitQuality=computed_info['rate_commit'],
        )
        team_repo.save()
        print(team_repo)
        # Add the TeamRepo instance to the current team
        team.repos.add(team_repo)

    return redirect("/")

@login_required(login_url="/login")
def suppressTeam(request):
    user = request.user
    coach = CoachCas.objects.get(user=user)

    # Retrieve the team to suppress
    team_name = request.GET.get('teamName','None')
    team = coach.teams.get(teamName=team_name)

    coach.teams.remove(team)
    
    coach.save()

    return redirect("/")


@login_required(login_url="/login")
def team_view(request):
    # Assuming the logged-in user is a coach
    user = request.user 
    coach = CoachCas.objects.get(user=user) 
    
    # Retrieve the team
    team_name = request.GET.get('teamName','None')
    team = coach.teams.get(teamName=team_name)

    # Create dictionaries to store users, moods, and repos for each team
    data = {}
    gitlab_access_repo_info = {}

    # Retrieve users, moods, and repos for each team
    users = team.users.all()
    moods = team.moods.all()
    repos = team.repos.all()
    if repos:
        last_repo = repos.latest('timeStamp')
    else:
        last_repo = repos
    
    # Retrieve GitLab information using the stored GitLab access token and repository URL
    gitlab_repo = team.gitlabRepo

    # Retrieve information from the GitlabAccessRepo model
    gitlab_access_repo_info = {
        'token': gitlab_repo.token,
        'url': gitlab_repo.url,
        'projectName': gitlab_repo.projectName,
    }
    
    data['team'] = {
        'name':team_name,
        'users': users,
        'moods': moods,
        'repo': last_repo,
        'gitlab_access_repo_info': gitlab_access_repo_info,
    }
    
    data['coach'] = {'user': coach.user.username}    

    return render(request, 'dashboard/repo.html', {'data': data})


@login_required(login_url="/login")
def add_team(request):
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





@redirect_authenticated_user
def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user  , backend='django.contrib.auth.backends.ModelBackend')
            return redirect("/")

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
            projectName = serializer.validated_data['projectName']
            
            # Fetch GitlabAccessRepo by projectName
            try:
                #repo = GitlabAccessRepo.objects.get(projectName=projectName)
                repos = GitlabAccessRepo.objects.filter(projectName=projectName)
            except GitlabAccessRepo.DoesNotExist:
                return Response({'status': 'error', 'message': 'Repo not found for the given projectName'}, 
                                status=status.HTTP_404_NOT_FOUND)
            
            for repo in repos:
                team = repo.gitlabAccess.first()
                
                if team:
                    mood = TeamMood.objects.create(timeStamp=datetime.datetime.now(), moodLevel=moodLevel, message=message)
                    team.moods.add(mood)
                
            return Response({'status': 'success',
                            'message': 'Data received and processed successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            # Invalid data
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#@require_http_methods(["GET", "POST"])

# views.py
#https://gitlab.paris-digital-lab.com
#glpat-GdDcjCKWycUxtFzpqvnG

@login_required(login_url="/login")
def add_new_token(request):
    if request.method == 'GET':
        # If the method is GET, redirect to a new page to display repositories
        form = GitlabAccessRepoForm()
        return render(request, "dashboard/token_form.html", {'form': form})

    elif request.method == 'POST' and 'selected_repos' in request.POST:
        selected_repos = request.POST.getlist('selected_repos')
       
        # Save the selected repositories to the database
        for repo in selected_repos:
            repo = repo.strip(" ").strip("[").strip("]").split(',')
            for i in range(len(repo)):
                repo[i] = repo[i].strip("`").strip("'").strip("'")

            data_dict = {
            'token': request.POST.get('token', ''),
            'url': request.POST.get('url', ''),
            'projectName':repo[0],
            }

            
            gitlab_access_repo = GitlabAccessRepo(
                token=data_dict["token"],
                url=data_dict["url"],
                projectName=data_dict["projectName"]
            )
            gitlab_access_repo.save()

            # Create TeamTable
            team_table = TeamTable(
                teamName=repo[0],
                gitlabRepo=gitlab_access_repo
            )
            team_table.save()

            print("RESPONSE ", repo)
            # Split the repo string to get individual usernames

            # Add users to TeamTable
            for username in repo[1:]:
                # print("USER ", username)
                user, created = Utilisateur.objects.get_or_create(username=username.replace("'",""))
                team_table.users.add(user)

            # Add TeamTable to the teams of the currently logged-in coach
            coach = CoachCas.objects.get(user=request.user) 

            coach.teams.add(team_table)

        return redirect("/")  # Redirect to the dashboard or 

    elif request.method == 'POST':
        # If the method is POST, validate the form
        form = GitlabAccessRepoForm(request.POST)

        if form.is_valid():
            # If the form is valid, get the list of repositories
            res = gitAPI.list_projects_users(form.cleaned_data['url'], form.cleaned_data['token'])

            # Pass the list of repositories to a new template for selection
            return render(request, "dashboard/select_repositories.html", {'form': form, 'repos': res})
        else:
            # If the form is not valid, return to the form with errors
            return render(request, "dashboard/token_form.html", {'form': form})

    # Handle the case when the user submits the form with selected repositories
   

    # Default case, return to the same page
    form = GitlabAccessRepoForm()
    return render(request, "dashboard/token_form.html", {'form': form})
    
