from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Skill
from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile,Team

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['branch', 'contact','languages', 'achievements', 'resume', 'profile_photo']



        
from django import forms
from .models import Skill

class AddSkillForm(forms.Form):
    existing_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_existing_skills'}),
        required=False,
        label="Select Skills"
    )
    new_skill = forms.CharField(
        max_length=100,
        required=False,
        label="If not listed, add your skill",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your skill (e.g., React Native, AI/ML, etc.)',
            'id': 'id_new_skill'
        })
    )
    languages = forms.CharField(
        max_length=200,
        required=False,
        label="Programming Languages Known",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    achievements = forms.CharField(
        required=False,
        label="Achievements",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    resume = forms.FileField(
        required=False,
        label="Upload Resume (PDF)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )





class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter team name', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your team', 'class': 'form-control', 'rows': 3}),
        }




from django import forms
from django.contrib.auth.models import User
from .models import Team

class AddMemberForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Select Student",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
