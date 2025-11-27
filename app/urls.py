from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.home.as_view(),name='home'),
    path('dashboard/',views.dashboard.as_view(),name='dashboard'),
    path('signup/',views.SignUpView.as_view(),name='signup')
]