from django.contrib import admin
from django.urls import path, include   # ✔ CORRECT

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('trainings/', include('trainings.urls')),
    path('reports/', include('reports.urls')),
    path('smart/',include('smart.urls')),
    path('trainer/',include('trainer.urls')),
    path('trainee/',include('trainee.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




