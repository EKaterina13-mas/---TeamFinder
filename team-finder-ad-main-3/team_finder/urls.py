from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.generic import RedirectView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/projects/list/", permanent=False)),
    path("users/", include("users.urls")),
    path("projects/", include("projects.urls")),
]

# Django's static() helper silently no-ops when DEBUG=False, no matter how
# it's called — so we register the view directly to actually serve media
# (avatars) in production too. Для крупного продакшена аватарки лучше
# хранить в облаке (S3 и т.п.), но для учебного демо этого достаточно.
urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]