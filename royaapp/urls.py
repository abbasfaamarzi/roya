from django.urls import path

from . import views

app_name = 'royaapp'

urlpatterns = [
    path('', views.index, name='index'),
]
