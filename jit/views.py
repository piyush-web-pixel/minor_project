from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UserRegisterForm, StudentProfileForm, AddSkillForm,Team
from .models import Skill, StudentProfile,Team
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm  # Only the user form
# from .models import Team
from .forms import TeamForm,AddMemberForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            messages.success(request, "Registration successful! Please log in to continue.")
            return redirect('login')  # ✅ Redirect to login page after registration
    else:
        user_form = UserRegisterForm()
    
    return render(request, 'register.html', {'user_form': user_form})









from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import StudentProfile, Skill
from .forms import AddSkillForm

@login_required
def add_skills(request):
    profile = StudentProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = AddSkillForm(request.POST, request.FILES)
        if form.is_valid():
            # Add existing skills
            for skill in form.cleaned_data['existing_skills']:
                profile.skills.add(skill)

            # Add new skill if provided
            new_skill = form.cleaned_data['new_skill']
            if new_skill:
                skill_obj, created = Skill.objects.get_or_create(name=new_skill.strip())
                profile.skills.add(skill_obj)

            # Update languages and achievements
            profile.languages = form.cleaned_data['languages']
            profile.achievements = form.cleaned_data['achievements']

            # Upload resume if provided
            if request.FILES.get('resume'):
                profile.resume = request.FILES['resume']

            profile.save()
            return redirect('my_profile')  # redirect to profile page after saving

    else:
        # Pre-fill form with existing data
        form = AddSkillForm(initial={
            'languages': profile.languages,
            'achievements': profile.achievements,
        })

    return render(request, 'add_skills.html', {'form': form})



from django.shortcuts import render
from jit.models import StudentProfile, Skill  # adjust the import according to your app

def search_students(request):
    query = request.GET.get('skill')
    
    if query:
        # Filter students by skill if query exists
        skill = Skill.objects.filter(name__icontains=query).first()
        if skill:
            students = StudentProfile.objects.filter(skills=skill)
        else:
            students = StudentProfile.objects.none()  # no matching skill
    else:
        # Show all registered students if no search query
        students = StudentProfile.objects.all()
    
    return render(request, 'search.html', {'students': students})




# @login_required
# def my_profile(request):
#     profile = StudentProfile.objects.get(user=request.user)
#     return render(request, 'my_profile.html', {'profile': profile})



from django.contrib.auth.decorators import login_required
from .models import StudentProfile

@login_required
def my_profile(request):
    # Try to get profile; if not exist, create one automatically
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'my_profile.html', {'profile': profile})





from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect after login
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')





from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')





def landing(request):
    return render(request, 'landing.html')



def dashboard(request):
    # Show latest 6 registered students
    latest_students = StudentProfile.objects.order_by('-id')[:6]
    teams = Team.objects.all()  # Get all teams
    return render(request, 'dashboard.html', {'latest_students': latest_students,'teams': teams})




def profile_detail(request, id):
    # Get the student or 404 if not found
    student = get_object_or_404(StudentProfile, id=id)
    return render(request, 'profile_detail.html', {'profile': student})






@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        
        if profile_form.is_valid():
            profile_form.save()
            return redirect('my_profile')
    else:
        profile_form = StudentProfileForm(instance=profile)
    
    return render(request, 'edit_profile.html', {'profile_form': profile_form, 'profile': profile})








@login_required
def create_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.creator = request.user
            team.save()
            team.members.add(request.user)  # Add creator as member
            return redirect('my_teams')
    else:
        form = TeamForm()
    return render(request, 'create_team.html', {'form': form})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Team

@login_required
def my_teams(request):
    # Teams created by the user
    created_teams = Team.objects.filter(creator=request.user)

    # Teams the user joined (but did not create)
    joined_teams = Team.objects.filter(members=request.user).exclude(creator=request.user)

    return render(request, 'my_teams.html', {
        'created_teams': created_teams,
        'joined_teams': joined_teams,
    })




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Team, StudentProfile
from django.contrib.auth.models import User
from .forms import AddMemberForm
from django.db.models import Q

@login_required
def add_member_to_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Only the creator can add members
    if request.user != team.creator:
        messages.error(request, "Only the team creator can add members.")
        return redirect('my_teams')

    students = None
    query = request.GET.get('q', '')

    # Search functionality
    if query:
        students = StudentProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        try:
            student = StudentProfile.objects.get(id=student_id)
            if student.user in team.members.all():
                messages.warning(request, f"{student.user.username} is already in the team.")
            else:
                team.members.add(student.user)
                messages.success(request, f"{student.user.username} added successfully to {team.name}.")
        except StudentProfile.DoesNotExist:
            messages.error(request, "Selected student does not exist.")
        return redirect('add_member', team_id=team.id)

    return render(request, 'add_member.html', {'team': team, 'students': students, 'query': query})





@login_required
def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'team_detail.html', {'team': team})




@login_required
def team_members(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'team_members.html', {'team': team})









@login_required
def remove_member(request, team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    member = get_object_or_404(User, id=user_id)

    if request.user != team.creator:
        messages.error(request, "Only the team leader can remove members.")
        return redirect('team_members', team_id=team.id)

    if member == team.creator:
        messages.error(request, "You cannot remove the team leader.")
        return redirect('team_members', team_id=team.id)

    team.members.remove(member)
    messages.success(request, f"{member.username} has been removed from {team.name}.")
    return redirect('team_members', team_id=team.id)





@login_required
def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user != team.creator:
        messages.error(request, "Only the team leader can delete this team.")
        return redirect('my_teams')

    if request.method == 'POST':
        team.delete()
        messages.success(request, f"Team '{team.name}' has been deleted.")
        return redirect('my_teams')

    return render(request, 'confirm_delete_team.html', {'team': team})





