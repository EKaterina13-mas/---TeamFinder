import json
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Project, Skill
from .forms import ProjectForm


PAGINATE_BY = 12
AUTOCOMPLETE_LIMIT = 10


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = PAGINATE_BY
    ordering = ['-created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        skill_name = self.request.GET.get('skill')
        if skill_name:
            qs = qs.filter(skills__name=skill_name)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        skill_name = self.request.GET.get('skill')
        context['all_skills'] = Skill.objects.order_by('name')
        context['active_skill'] = skill_name
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'
    context_object_name = 'project'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.object.participants.add(self.request.user)
        return response

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


def skills_autocomplete(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse([], safe=False)
    
    skills_qs = (
        Skill.objects
        .filter(name__istartswith=query)
        .order_by('name')
        .values('id', 'name')[:AUTOCOMPLETE_LIMIT] 
    )
    return JsonResponse(list(skills_qs), safe=False)


@method_decorator(login_required, name='dispatch')
class ProjectSkillAddView(View):
    @transaction.atomic
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if project.owner != request.user:
            return JsonResponse(
                {'error': 'Permission denied'},
                status=HTTPStatus.FORBIDDEN
            )

        data = {}

        # если данные пришли как обычная форма
        if request.POST:
            data.update(request.POST.dict())

        # если данные пришли как JSON
        if request.body:
            try:
                body_data = json.loads(request.body.decode('utf-8'))
                if isinstance(body_data, dict):
                    data.update(body_data)
            except json.JSONDecodeError:
                pass

        print("ADD SKILL DATA:", data)

        skill_id = data.get('skill_id') or data.get('id')

        skill_name = (
            data.get('name')
            or data.get('skill_name')
            or data.get('skillName')
            or data.get('text')
            or data.get('value')
            or data.get('label')
            or ''
        )

        if isinstance(skill_name, str):
            skill_name = skill_name.strip()

        created = False
        added = False
        skill = None

        if skill_id:
            skill = get_object_or_404(Skill, id=skill_id)

        elif skill_name:
            skill, created = Skill.objects.get_or_create(name=skill_name)

        if not skill:
            return JsonResponse(
                {
                    'error': 'Skill not provided',
                    'received_data': data,
                },
                status=HTTPStatus.BAD_REQUEST
            )

        if not project.skills.filter(id=skill.id).exists():
            project.skills.add(skill)
            added = True

        return JsonResponse({
            'id': skill.id,
            'skill_id': skill.id,
            'name': skill.name,
            'skill_name': skill.name,
            'created': created,
            'added': added,
        })


@method_decorator(login_required, name='dispatch')
class ProjectToggleParticipateView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if project.owner_id == request.user.id:
            return JsonResponse(
                {'error': 'Owner cannot toggle participation'},
                status=HTTPStatus.BAD_REQUEST,
            )

        if project.participants.filter(id=request.user.id).exists():
            project.participants.remove(request.user)
            is_participant = False
        else:
            project.participants.add(request.user)
            is_participant = True

        return JsonResponse({
            'status': 'ok',
            'participant': is_participant,
            'participants_count': project.participants.count(),
        })


@method_decorator(login_required, name='dispatch')
class ProjectCompleteView(View):
    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        if project.owner_id != request.user.id:
            return JsonResponse(
                {'error': 'Permission denied'},
                status=HTTPStatus.FORBIDDEN,
            )

        project.status = 'closed'
        project.save(update_fields=['status'])

        return JsonResponse({'status': 'ok', 'project_status': project.status})


@method_decorator(login_required, name='dispatch')
class ProjectSkillRemoveView(View):
    def post(self, request, project_id, skill_id):
        project = get_object_or_404(Project, id=project_id)
        skill = get_object_or_404(Skill, id=skill_id)
        
        if project.owner != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=HTTPStatus.FORBIDDEN)
        
        if not project.skills.filter(id=skill_id).exists():
            return JsonResponse({'error': 'Skill not linked to project'}, status=HTTPStatus.NOT_FOUND)
        
        project.skills.remove(skill)
        return JsonResponse({'status': 'removed'})