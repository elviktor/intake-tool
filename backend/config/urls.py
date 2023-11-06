from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from upload.views import image_upload

urlpatterns = [
    #path("", image_upload, name="upload"),
    # Django admin
    path('admin/', admin.site.urls),

    # User management
    path('accounts/', include('allauth.urls')),

    # API
    path('v0/', include('api.urls')),

    # Local apps
    path("tracker/", include('tracker.urls')),
    path("intakemanager/", include('intakemanager.urls')),
    path("intake/", include('intake.urls')),
    path("accounts/", include('accounts.urls')),
    path("", include('pages.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
