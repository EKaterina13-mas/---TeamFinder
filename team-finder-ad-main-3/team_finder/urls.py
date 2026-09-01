from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/projects/list/", permanent=False)),
    path("users/", include("users.urls")),
    path("projects/", include("projects.urls")),
]

# Для крупного продакшена аватарки лучше хранить в облаке (S3 и т.п.),
# но для учебного демо-проекта с невысокой нагрузкой отдаём их прямо
# через Django и в DEBUG=False тоже — иначе картинки не будут видны на сайте.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)