from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_event_data, name='home'),   
]