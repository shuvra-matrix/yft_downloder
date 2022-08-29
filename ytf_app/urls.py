from django.contrib import admin
from django.urls import path
from ytf_app import views

app_name = 'ytf'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
]
