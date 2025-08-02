from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name="home"),      #here first value is null because it is landing page
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    #below is the urls of all exam card module

    path('exam/', views.exam, name="exam"),
    path('exam/<int:subject_id>/', views.start_exam, name='start_exam'),
    path('submit_exam/<int:subject_id>/', views.submit_exam, name='submit_exam'),
    path('profile/', views.profile_view, name='profile'),

    # to make about us module url 
    path('about/', views.about_us, name='about_us'),
    #to make result module url
    path('results/', views.result_list, name='result_list'),

    #to make contact module url
    path('contact/', views.contact, name='contact'),




]