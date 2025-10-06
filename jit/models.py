from django.contrib.auth.models import User
from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    skills = models.ManyToManyField(Skill, blank=True)
    languages = models.CharField(max_length=200, blank=True)  # e.g., Python, C++, Java
    achievements = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # PDF resume
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    


    def __str__(self):
        return self.user.username




class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams')
    members = models.ManyToManyField(User, related_name='teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    







class TeamJoinRequest(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} → {self.team.name}"
