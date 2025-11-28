from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.signinView.as_view(),name='signin'),
    path('home/',views.home.as_view(),name='home'),
    path('dashboard/',views.dashboard.as_view(),name='dashboard'),
    path('edit_item/<int:pk>/',views.edit_item.as_view(),name='edititem'),
    path('delete_item/<int:pk>/',views.delete_item.as_view(),name='deleteitem'),
    path('add-item/', views.add_item.as_view(), name='additem'),
    #Authentication
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('signin/',views.signinView.as_view(),name='signin'),
    path('signout/',views.signoutView.as_view(),name='signout'),
    
]