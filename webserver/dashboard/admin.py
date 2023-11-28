from django.contrib import admin
from .models import TeamMood, TeamRepo, TeamTable, Utilisateur, Coach, GitlabAccessRepo

# Register your models here.

@admin.register(Coach)
class CoachModelAdmin(admin.ModelAdmin):
    list_display = ('username',)

@admin.register(Utilisateur)
class UtilisateurModelAdmin(admin.ModelAdmin):
    list_display = ('username',)

@admin.register(GitlabAccessRepo)
class GitlabAccessRepoModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'url', 'projectName')  # Add fields to customize the display

@admin.register(TeamTable)
class TeamTableModelAdmin(admin.ModelAdmin):
    list_display = ('teamId', 'teamName')

@admin.register(TeamMood)
class TeamMoodModelAdmin(admin.ModelAdmin):
    list_display = ('timeStamp', 'moodLevel', 'message')

@admin.register(TeamRepo)
class TeamRepoModelAdmin(admin.ModelAdmin):
    list_display = ('timeStamp', 'branchNumber', 'branchBehindMax', 'branchAheadMax', 'lastPrTime', 'commitQuality')
