from django.db import models
from django.contrib.auth.models import User, BaseUserManager




class Utilisateur(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.username

class GitlabAccessRepo(models.Model):
    id = models.AutoField(primary_key=True)  
    token = models.CharField(max_length=255)
    url = models.URLField()
    projectName = models.CharField(max_length=255)



class TeamMood(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)
    moodLevel = models.IntegerField()
    message = models.TextField()

    def __str__(self):
        return f"{self.moods.first().teamName} - {self.timeStamp}"


class TeamRepo(models.Model):
    timeStamp = models.DateTimeField(auto_now_add=True)
    branchNumber = models.IntegerField()
    branchBehindMax = models.IntegerField()
    branchAheadMax = models.IntegerField()
    lastPrTime = models.DateTimeField(null=True, blank=True)
    commitQuality = models.IntegerField()

    def __str__(self):
        return f"TeamRepo - {self.timeStamp}"


class TeamTable(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=255, unique=True)
    gitlabRepo = models.ForeignKey(GitlabAccessRepo, related_name="gitlabAccess", on_delete=models.CASCADE, unique=False)
    users = models.ManyToManyField(Utilisateur, related_name='teams', blank=True)
    moods = models.ManyToManyField(TeamMood , related_name="moods" , blank=True ) 
    repos = models.ManyToManyField(TeamRepo , related_name="repos" , blank=True )
    def __str__(self):
        return self.teamName

#OBJECTIVE     
class Coach(User):    
    teams = models.ManyToManyField(TeamTable , related_name='teams' , blank=True)

    def __str__(self):
        return self.username
    


