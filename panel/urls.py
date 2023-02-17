from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.dashBoard, name='dashboard'),
    path('login/', views.loginUser, name='loginUser'),
    path('logout/', views.logoutApp, name='logout'),
    path('books/', views.books, name='books'),
    path('bookings/', views.bookings, name='bookings'),
    path('profile/', views.profile, name='profile'),
    path('view_profile/', views.viewProfile, name='view_profile'),
    path('wallet/', views.wallet, name='wallet'),
    path('pass_reset/', views.passReset, name='pass_reset'),
    path('signup/', views.signUp, name='signup'),
    path('pass_reset_confirmation/', views.passResetConfirm, name='pass_reset_confirmation'),
    path('pass_reset_done/', views.passResetDone, name='pass_reset_done'),
    path('pass_reset_sent/', views.passResetSent, name='pass_reset_sent'),
    path('activity_log/', views.activityLog, name='activity_log'),
    path('add_book/', views.addBook, name='add_book'),
    path('add_student/', views.addStudent, name='add_student'),
    path('add_booking/', views.addBooking, name='add_booking'),
    path('students/', views.students, name="students"),

]
