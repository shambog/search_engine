from django.conf.urls import url, include
from django.urls import path
from . import views

#this file is related to Django framework

app_name = 'personal'
urlpatterns = [
    path('', views.index, name='index'),
    path('<tosearch>/', views.search, name='search'),
    path('<reldoc>/<reldoc1>/', views.relevance, name='relevance')    
]
