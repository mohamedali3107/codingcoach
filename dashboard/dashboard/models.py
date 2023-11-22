from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CoachTableManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse e-mail doit être spécifiée.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
    

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


class CoachTable(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=128)  # Utilisez plutôt models.PasswordField()
    teams = models.ManyToManyField(TeamTable, related_name='teams', blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CoachTableManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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

