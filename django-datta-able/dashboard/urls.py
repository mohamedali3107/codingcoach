from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views
app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),

    # URL pour la création d'un coach
    path('create_coach/', views.create_coach, name='create_coach'),

    # URL pour la création d'une team
    path('create_team/', views.create_team, name='create_team'),

    # Autres URLs liées à l'authentification (inscription, connexion, déconnexion, etc.)
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls)

    # Ajoutez d'autres URLs au besoin
]
