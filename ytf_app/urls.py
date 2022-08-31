from django.contrib import admin
from django.urls import path
from ytf_app import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ytf'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ytdown', views.ydown, name='ytdown'),
    path('ytdownload', views.ytdownload, name='ytdownload'),
    path('downloadyt', views.yvdown, name='yvdown'),
    path('ytmusic', views.ytmusic, name='ytmusic'),
    path('ytmsearch', views.ytmsearch, name='ytmsearch'),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
