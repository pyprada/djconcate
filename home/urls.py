from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [
    path('', views.home, name='home'),
    path('quiz', views.quiz, name='quiz'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('search', views.search, name='search'),
    path('signup', views.submitSignup, name='signup'),
    path('login', views.submitLogin, name='login'),
    path('logout', views.submitLogout, name='logout'),


  ]