from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm

import re

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ('name', 'surname', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Неверный имейл или пароль",
    }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            return phone
            
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        if not re.match(r'^(\+7|8)\d{10}$', phone):
            raise forms.ValidationError("Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX")
            
        if phone.startswith('8'):
            phone = '+7' + phone[1:]
            
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот номер телефона уже зарегистрирован")
            
        return phone

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url:
            if 'github.com' not in url.lower():
                raise forms.ValidationError("Ссылка должна вести на GitHub")
        return url