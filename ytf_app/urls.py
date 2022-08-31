from django.contrib import admin
from django.urls import path
from ytf_app import viewsaa
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ytf'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', viewsaa.index, name='index'),
    path('ytdown', viewsaa.ydown , name='ytdown'),
    path('ytdownload',viewsaa.ytdownload, name = 'ytdownload'),
    path('downloadyt',viewsaa.yvdown,name='yvdown'),
]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
