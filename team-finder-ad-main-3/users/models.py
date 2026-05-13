import io
import random

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .utils import generate_avatar


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, surname, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            name=name, 
            surname=surname, 
            phone=phone, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='Email')
    name = models.CharField(max_length=124, verbose_name='Имя')
    surname = models.CharField(max_length=124, verbose_name='Фамилия')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    phone = models.CharField(max_length=12, verbose_name='Телефон')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    about = models.TextField(max_length=256, blank=True, verbose_name='О себе')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Администратор')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'phone']
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-id']
    
    def __str__(self):
        return f'{self.surname} {self.name}'
    
    def save(self, *args, **kwargs):
        # Генерируем аватар при создании пользователя, если он не загружен вручную
        if not self.pk and not self.avatar:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)