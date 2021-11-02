from django.urls import path 
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('/retrain', views.retrain_model, name='retrain')
]
