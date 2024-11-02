from django.contrib import admin
from django.urls import path
from uploader import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.file_upload_view, name='file_upload'), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

