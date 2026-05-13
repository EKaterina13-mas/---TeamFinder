from django import forms

from .models import Project


STATUS_CHOICES = [('open', 'Открыт'), ('closed', 'Закрыт')]


class ProjectForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Статус')

    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            if 'github.com' not in url.lower():
                raise forms.ValidationError("Ссылка должна вести на GitHub")
        return url