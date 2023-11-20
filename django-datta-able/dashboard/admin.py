from django.contrib import admin
from .models import CoachTable, Utilisateur, TeamTable, TeamMood, TeamRepo

# Register your models here.

@admin.register(CoachTable)
class CoachModelAdmin(admin.ModelAdmin):
    list_display = ('username',)  # Customize the fields to display

@admin.register(Utilisateur)
class UtilisateurModelAdmin(admin.ModelAdmin):
    list_display = ('username',)  # Customize the fields to display

@admin.register(TeamTable)
class TeamTableModelAdmin(admin.ModelAdmin):
    list_display = ('teamId',)  # Customize the fields to display

@admin.register(TeamMood)
class TeamModelAdmin(admin.ModelAdmin):
    list_display = ('timeStamp',)  # Customize the fields to display

@admin.register(TeamRepo)
class TeamRepoModelAdmin(admin.ModelAdmin):
    list_display = ('timeStamp',)  # Customize the fields to display