from django.http import HttpRequest
from .forms import RegisterForm, TeamTableForm
from django.shortcuts import redirect, render
from django.contrib.auth import login , logout , authenticate 
from django.contrib.auth.decorators import login_required , user_passes_test
# Create your views here.

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