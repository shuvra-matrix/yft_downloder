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
    path('ytmusic', views.ytmusic, name='ytmusic'),
    path('ytmsearch', views.ytmsearch, name='ytmsearch'),
    path('fbsearch', views.fbsearch, name='fbsearch'),
    path('twitter_search', views.twisearch, name='twisearch'),
    path('admins', views.admins, name='admins'),
    path('offline/', TemplateView.as_view(template_name="offline.html")),

]
