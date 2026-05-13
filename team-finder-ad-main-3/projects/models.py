from django.db import models
from django.conf import settings


STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]


class Skill(models.Model):
    name = models.CharField(max_length=124, unique=True, verbose_name='Навык')
    
    class Meta:
        verbose_name = 'Навык проекта'
        verbose_name_plural = 'Навыки проектов'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название проекта')
    description = models.TextField(blank=True, verbose_name='Описание')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name='Автор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    github_url = models.URLField(blank=True, null=True, verbose_name='GitHub')
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, verbose_name='Статус')
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='projects',
        verbose_name='Необходимые навыки'
    )
    
    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.name