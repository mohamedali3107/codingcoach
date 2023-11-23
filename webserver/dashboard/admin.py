from django.contrib import admin

from .models import TeamMood, TeamRepo, TeamTable, Utilisateur
from .models import Coach

# Register your models here.
@admin.register(Coach)
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
