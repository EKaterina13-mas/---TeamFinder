from django.urls import path

from .views import (
    ProjectListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, skills_autocomplete, ProjectSkillAddView,
    ProjectSkillRemoveView,
)

urlpatterns = [
    path('list/', ProjectListView.as_view(), name='project_list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('create-project/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),
    path('skills/', skills_autocomplete, name='skills_autocomplete'),
    path('<int:project_id>/skills/add/', ProjectSkillAddView.as_view(), name='project_skill_add'),
    path('<int:project_id>/skills/<int:skill_id>/remove/', ProjectSkillRemoveView.as_view(), name='project_skill_remove'),
]