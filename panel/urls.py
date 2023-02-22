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
    path('add_book/', views.addBook, name='add_book'),
    path('add_student/', views.addStudent, name='add_student'),
    path('add_booking/', views.addBooking, name='add_booking'),
    path('register/', views.registerStudent, name='registerStudent'),
    path('students/', views.students, name="students"),
    path('returnBook/', views.returnBook, name='returnBook')

]
