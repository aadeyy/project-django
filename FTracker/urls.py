from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('finance/', views.finance, name='finance'),
]