from django.urls import path
from . import views

urlpatterns=[
     path('', views.index),
     path('extract1',views.extract1),
]