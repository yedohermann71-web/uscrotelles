from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('infos/', views.infos, name='infos'),
    path('matchs/', views.matchs, name='matchs'),
    path('classement/', views.classement, name='classement'),
    path('contact/', views.contact, name='contact'),
]