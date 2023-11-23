from django.db import models
from django.contrib.auth.models import User, BaseUserManager




#MODEL DES ELEVES
class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username
    

class TeamTable(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=255, unique=True)
    teamGitlabAccessToken = models.CharField(max_length=255)
    users = models.ManyToManyField(Utilisateur, related_name='teams', blank=True)

    def __str__(self):
        return self.teamName

#OBJECTIVE     
class Coach(User):    
    teams = models.ManyToManyField(TeamTable , related_name='teams' , blank=True)
    def __str__(self):
        return self.username
    


class TeamMood(models.Model):
    teams = models.ManyToManyField(TeamTable, related_name='moods')
    timeStamp = models.DateTimeField(auto_now_add=True)
    moodLevel = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.teams.first().teamName} - {self.timeStamp}"


class TeamRepo(models.Model):
    teams = models.ManyToManyField(TeamTable, related_name='repos')
    timeStamp = models.DateTimeField(auto_now_add=True)
    branchNumber = models.IntegerField()
    branchBehindMax = models.IntegerField()
    branchAheadMax = models.IntegerField()
    lastPrTime = models.DateTimeField(null=True, blank=True)
    commitQuality = models.IntegerField()

    def __str__(self):
        return f"TeamRepo - {self.timeStamp}"

