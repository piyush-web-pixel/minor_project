from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # path('search/', views.search_students, name='search'),
    path('register/', views.register, name='register'),
    path('add-skills/', views.add_skills, name='add_skills'),
    path('search/', views.search_students, name='search_students'),
        # path('add-skills/', views.add_skills, name='add_skills'),
    path('my-profile/', views.my_profile, name='my_profile'),
    # urls.py
    path('profile/<int:id>/', views.profile_detail, name='profile_detail'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # ... existing paths ...
    path('create-team/', views.create_team, name='create_team'),
    path('my-teams/', views.my_teams, name='my_teams'),


    path('team/<int:team_id>/add-member/', views.add_member_to_team, name='add_member'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('team/<int:team_id>/members/', views.team_members, name='team_members'),
    path('team/<int:team_id>/remove-member/<int:user_id>/', views.remove_member, name='remove_member'),
    path('team/<int:team_id>/delete/', views.delete_team, name='delete_team'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
