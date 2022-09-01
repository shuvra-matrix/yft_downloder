from django.contrib import admin
from django.urls import path
from ytf_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

app_name = 'ytf'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ytdown', views.ydown, name='ytdown'),
    path('ytdownload', views.ytdownload, name='ytdownload'),
    path('downloadyt', views.yvdown, name='yvdown'),
    path('ytmusic', views.ytmusic, name='ytmusic'),
    path('ytmsearch', views.ytmsearch, name='ytmsearch'),
    path('offline/', TemplateView.as_view(template_name="offline.html")),

]


if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
