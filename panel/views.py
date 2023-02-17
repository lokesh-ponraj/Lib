from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from panel.qSort import qSort
from django.contrib.auth import logout,login,authenticate
from panel.decorators import unAuthenticatedUser
from django.contrib.auth.decorators import login_required
from .models import Student, Book, Borrow
# Create your views here.


def updateFine():
    borrows = list(Borrow.objects.all())
    for b in borrows:
        if b.dueDate < timezone.now().date():
            diff = datetime.now.date() - b.dueDate
            fine = diff.days * 1
            b.fineAmount = fine
            b.save()

@login_required(login_url='login')
def dashBoard(request):
    updateFine()
    stud  = Student.object.get(user = User.objects.get(id = request.user.id))
    bookCount = Book.objects.count
    borrowCount = Borrow.objects.filter(borrower = stud).count
    pendingReturns = 0
    borrows = list(Borrow.objects.filter(borrower = stud))

    # Total fine collection
    borrowFine = list(Borrow.objects.filter(borrower = stud).values_list('fine_amount', flat=True))
    totalFine = sum(borrowFine)

    # Finding the pending return of books
    for s in borrowFine:
        if s > 0:
            pendingReturns += 1
        qSort(borrows, 'fine_amount')
        borrows = borrows[-5:]


    # Books in demand
    demandBooks = list(Borrow.objects.filter(borrower = stud).values_list('book', flat=True))
    data = {'bookCount': bookCount, 'borrowCount':borrowCount, 'totalFine':totalFine, 'pendingReturns':pendingReturns, 'fullName':stud.fullName}
    if pendingReturns !=0:
        data['borrows'] = borrows
    if len(demandBooks) !=0:
        data['demandBooks'] = demandBooks
    data['fullName'] = stud.fullName

    return render(request ,'panel/dashboard.html')
# User Login
@unAuthenticatedUser
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashBoard)
        else:
            return render(request, 'panel/login.html',{'message':'Invalid credentials'})
    return render (request, 'panel/login.html')

@login_required(login_url='login')
def books(request):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    books = list(Book.objects.all())
    if request.method == 'POST':
        key = request.POST.get('sort_by')
        qSort(books, key.lower())
    return render(request, 'panel/books.html', {'books':books, 'fullName':stud.fullName})


    

def bookings(request):
    return render(request, 'panel/bookings.html')

def profile(request):
    return render(request, 'panel/profile.html')

def viewProfile(request):
    return render(request, 'panel/view_profile.html')

def wallet(request):
    return render(request, 'panel/wallet.html')

def passReset(request):
    return render(request, 'panel/pass_reset.html')

def signUp(request):
    return render(request, 'panel/signup.html')

def passResetConfirm(request):
    return render(request, 'panel/pass_reset_confirm.html')

def passResetDone(request):
    return render(request, 'panel/pass_reset_done.html')

def passResetSent(request):
    return render(request, 'panel/pass_reset_sent.html')

def activityLog(request):
    return render(request, 'panel/activity_log.html')

def addBook(request):
    return render(request, 'panel/add_book.html')

def addStudent(request):
    return render(request, 'panel/add_student.html')

def addBooking(request):
    return render(request, 'panel/add_booking.html')

# Listing the students
@login_required(login_url='login')
def students(request):
    updateFine()
    students = list(Student.objects.all())
    stud_db = []
    for s in students:
        students_db = {}
        temp = list(Borrow.objects.filter(borrower = s).values_list('fine_amount',flat=True))
        students_db['fullName'] = s.fullName
        students_db['roll_number'] = s.rollNo
        
    return render(request, 'panel/students.html')

def logoutApp(request):
    logout(request)
    return redirect(login)