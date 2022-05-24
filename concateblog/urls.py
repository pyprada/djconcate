from django.contrib import admin
from django.urls import path, include
from .import views

urlpatterns = [
    
    path('', views.concateblogHome, name='concateblogHome'),
    path('postComment', views.postComment, name='postComment'),
    path('<str:slug>', views.concateblogPost, name='concateblogPost'),
    
    
  ]