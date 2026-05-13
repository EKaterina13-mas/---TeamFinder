from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, LogoutView
from django import views
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserEditForm


USERS_PER_PAGE = 12


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'
    paginate_by = USERS_PER_PAGE
    ordering = ['-id']


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'
    context_object_name = 'user'


class UserRegisterView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserLoginView(views.View):
    template_name = 'users/login.html'

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('project_list')
        return render(request, self.template_name, {'form': form})


class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'users/edit_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.object.pk})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    context_object_name = 'form'
    form_class = DjangoPasswordChangeForm

    def get_success_url(self):
        return reverse('user_detail', kwargs={'pk': self.request.user.pk})


class CustomLogoutView(LogoutView):
    next_page = '/projects/list/'