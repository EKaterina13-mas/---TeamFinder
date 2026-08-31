from django.core.management.base import BaseCommand
from django.db import transaction

from projects.models import Project, Skill
from users.models import User


DEMO_USERS = [
    {
        "email": "anna@example.com",
        "name": "Анна",
        "surname": "Иванова",
        "phone": "+79001112233",
        "github_url": "https://github.com/anna-example",
        "about": "Frontend-разработчик, люблю React и красивые интерфейсы.",
    },
    {
        "email": "boris@example.com",
        "name": "Борис",
        "surname": "Петров",
        "phone": "+79001112244",
        "github_url": "https://github.com/boris-example",
        "about": "Backend на Django, интересуюсь архитектурой API.",
    },
    {
        "email": "kate@example.com",
        "name": "Екатерина",
        "surname": "Смирнова",
        "phone": "+79001112255",
        "github_url": "https://github.com/kate-example",
        "about": "UI/UX-дизайнер, собираю команду для pet-проектов.",
    },
]

DEMO_SKILLS = ["Python", "Django", "React", "PostgreSQL", "Figma", "Docker"]

DEMO_PROJECTS = [
    {
        "owner_email": "anna@example.com",
        "name": "TeamFinder Mobile",
        "description": "Мобильная версия TeamFinder на React Native.",
        "status": "open",
        "skills": ["React", "Figma"],
    },
    {
        "owner_email": "boris@example.com",
        "name": "Recipe Sharing API",
        "description": "REST API для обмена рецептами с рейтингами и тегами.",
        "status": "open",
        "skills": ["Python", "Django", "PostgreSQL"],
    },
    {
        "owner_email": "kate@example.com",
        "name": "Design System Kit",
        "description": "Библиотека UI-компонентов для быстрого прототипирования.",
        "status": "closed",
        "skills": ["Figma"],
    },
]

DEFAULT_PASSWORD = "demo-password-123"


class Command(BaseCommand):
    help = "Создаёт тестовых пользователей и проекты для проверки ревьюером"

    @transaction.atomic
    def handle(self, *args, **options):
        skills_by_name = {}
        for name in DEMO_SKILLS:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills_by_name[name] = skill

        users_by_email = {}
        for data in DEMO_USERS:
            user, created = User.objects.get_or_create(
                email=data["email"],
                defaults={
                    "name": data["name"],
                    "surname": data["surname"],
                    "phone": data["phone"],
                    "github_url": data["github_url"],
                    "about": data["about"],
                },
            )
            if created:
                user.set_password(DEFAULT_PASSWORD)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Создан пользователь {user.email}"))
            users_by_email[data["email"]] = user

        for data in DEMO_PROJECTS:
            owner = users_by_email[data["owner_email"]]
            project, created = Project.objects.get_or_create(
                name=data["name"],
                owner=owner,
                defaults={
                    "description": data["description"],
                    "status": data["status"],
                },
            )
            if created:
                project.participants.add(owner)
                project.skills.set([skills_by_name[s] for s in data["skills"]])
                self.stdout.write(self.style.SUCCESS(f"Создан проект «{project.name}»"))

        self.stdout.write(self.style.SUCCESS(
            f"Готово. Пароль у всех демо-пользователей: {DEFAULT_PASSWORD}"
        ))
