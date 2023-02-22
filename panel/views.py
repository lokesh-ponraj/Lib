from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.forms import ValidationError
from datetime import datetime
from panel.qSort import qSort
from django.contrib.auth import logout,login,authenticate
from panel.decorators import unAuthenticatedUser
from django.contrib.auth.decorators import login_required
from .models import Student, Book, Borrow, Transaction
from django.contrib.auth.password_validation import validate_password
# Create your views here.


def updateFine():
    borrows = list(Borrow.objects.all())
    for b in borrows:
        if b.dueDate < timezone.now().date():
            diff = datetime.now.date() - b.dueDate
            fine = diff.days * 1
            b.fineAmount = fine
            b.save()

# @login_required(login_url='login')
@unAuthenticatedUser
def dashBoard(request):
    updateFine()
    stud  = Student.objects.get(user = User.objects.get(id= request.user.id))
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


# # Listing the books
# @login_required(login_url='login')
@unAuthenticatedUser
def books(request):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    books = list(Book.objects.all())
    if request.method == 'POST':
        key = request.POST.get('sort_by')
        qSort(books, key.lower())
    return render(request, 'panel/books.html', {'books':books, 'fullName':stud.fullName})


    
# Listing borrows
# @login_required(login_url='login')
def bookings(request):
    updateFine()
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    borrows = list(Borrow.onjects.filter(borrower = stud))
    if request.method == 'POST':
        key = request.POST.get('sort_by')
        qSort(borrows, key.lower())
        return render(request,'panel/bookings.html',{'borrows':borrows, 'fullName':stud.fullName})

# Student profile
# @login_required(login_url='login')
def profile(request):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    data = {}
    data['fullName'] = stud.fullName
    data['email'] = stud.email
    data['rollNo'] = stud.rollNo
    data['academicYear'] = stud.academicYear
    if request.method == 'POST':
        fullName = request.POST.get('fullName')
        rollNo = request.POST.get('rollNo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('password_cnfrm')
        academicYear = request.POST.get('academicYear')
        if fullName != '':
            stud.fullName = fullName
        else:
            data['error'] = 'Empty field (fullname) not permitted'
        if rollNo != '':
            stud.rollNo = rollNo
        else:
            data['error'] = 'Empty field (rollNo) not permitted'
        if email != '':
            stud.email = email
        else:
            data['error'] = 'Empty field (email) not permitted'

        if academicYear == '':
            data['error'] = 'Empty field (academic year) not permitted'
        else:
            stud.academicYear = academicYear
        
        if 'error' in data.keys():
            return render(request, 'panel/profile.html', data)
        stud.save()


         # Change password
        if password != '' and conf_pass != '' and password == conf_pass:
            try:
                val = validate_password(password)
                if val == None:
                    user = User.objects.get(id = request.user.id)
                    user.set_password(password)
                    user.save()
                    return redirect('dashboard')
            except ValidationError as v:
                data['error'] = '\n'.join(v)
                return render(request, 'panel/profile.html', data)

    return render(request, 'panel/profile.html', data)
@login_required(login_url='login')
def viewProfile(request):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    borrow_fine = list(Borrow.objects.filter(borrower = stud).values_list('fine_amount', flat=True))
    total_fine = sum(borrow_fine)
    return render(request, 'panel/profile.html',{
        'student':stud, 'fullName':stud.fullName,'total_fine':total_fine 
    })
   
@login_required(login_url='login')
def wallet(request):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    borrow_fine = list(Borrow.objects.filter(borrower = stud).values_list('fine_amount', flat=True))
    total_fine = sum(borrow_fine)
    transactions = Transaction.objects.filter(payer = stud)
    return render(request, 'panel/wallet.html',{
        'student':stud, 'fullName':stud.fullName,'total_fine':total_fine, 'transactions':transactions
    })

# Book adding
@login_required(login_url='login')
def addBook(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn_number = request.POST.get('isbn_number')
        copies = request.POST.get('copies')
        book = Book(
            isbn_number = isbn_number,
            title = title,
            author = author,
            copies = copies)
        
        book.save()
        return redirect('books')
    return render(request, 'panel/add_book.html')

# Students adding
@login_required(login_url='login')
def addStudent(request):
    if request.method == 'POST':
        fullName = request.POST.get('fullName')
        rollNo = request.POST.get('rollNo')
        academicYear = request.POST.get('academicYear')
        email = rollNo.lower() + '@ch.students.palib.edu'
        student = Student(
        fullName = fullName,
        rollNo = rollNo,
        academicYear = academicYear,
        email = email
        )
        student.save()
        return redirect('students')
    return render(request, 'panel/add_student.html')


# Make a booking
@login_required(login_url='login')
def addBooking(request, book_id):
    stud = Student.objects.get(user = User.objects.get(id = request.user.id))
    book = Book.objects.get(id = book_id)
    data = {'fullName':stud.fullName, 'book':book}
    if request.method == 'POST':
        borrower = request.POST.get('borrower')
        due_date = request.POST.get('due_date')
        # Checking the availablity
        bk = list(Borrow.objects.filter(book = book).values_list('book', flat=True))
        if len(bk) < book.copies:
            borrow = Borrow(
                borrower = Student.objects.get(fullName = borrower),
                due_date = due_date,
                book=Book.objects.get(title=book)
            )
            borrow.save()
            return redirect('bookings')
        else:
            data['error'] = 'The requested book is not in stock'
    return render(request, 'panel/add_booking.html', data)

# Returning books
@login_required(login_url='login')
def returnBook(request, borrow_id):
    brw = Borrow.objects.get(id = borrow_id)
    if brw.dueDate < timezone.now().date():
        color = 'red'
    else:
        color = 'green'
    if request.method == 'POST':
        stud = Student.objects.get(user = User.objects.get(id = request.user.id))
        if stud.balance >= brw.fineAmount:
            stud.balance = stud.balance - brw.fineAmount
            stud.save()
            tr = Transaction.objects.create(
                payer = stud,
                book = brw.book,
                amount = brw.fineAmount
            )
            tr.save()
            brw.delete()
            return redirect('bookings')
        else:
            return render(request, 'panel/return_book.html', {'borrow':brw, 'color':color, 'error':'Insufficient funds'})
    return render(request, 'panel/return_book.html', {'borrow':brw, 'color':color})

    
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
        students_db['rollNo'] = s.rollNo
        students_db['academicYear'] = s.academicYear
        students_db['email'] = s.email
        students_db['fine'] = sum(temp)
        students_db['id'] = s.id
        stud_db.append(students_db)

    if request.method == 'POST':
        key = request.POST.get('sort_by')
        qSort(students, key.lower())
    return render(request,'panel/students.html', {'students' : stud_db})
        

# Registration
def registerStudent(request):
    data={}
    if request.method == 'POST':
        fullName = request.POST.get('fullName')
        rollNo = request.POST.get('rollNo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conf_pass = request.POST.get('password_cmfrm')
        academicYear = request.POST.get('academicYear')
        if fullName == '':
            data['error'] = 'Empty field (fullname) not permitted'
        if rollNo == '':
            data['error'] = 'Empty field (rollno) not permitted'
        if email == '':
            data['error'] = 'Empty field (email) not permitted'
        if academicYear == '':
            data['error'] = 'Empty field (academic year) not permitted'
        if 'error' in data.keys():
            return render(request, 'panel/profile.html', data)
        # Password setting
        if password != '' and conf_pass != '' and password == conf_pass:
            try:
                val = validate_password(password)
                if val == None:
                    fullnamearr = fullName.split(' ')
                    firstname, lastname = fullnamearr[0],''.join(fullnamearr[1:])
                    user = User.objects.create_user(firstname[:10].lower(), email,password)
                    user.first_name = firstname
                    user.last_name = lastname
                    user.save()
                    st = Student.objects.create(
                        fullName = fullName,
                        rollNo = rollNo,
                        email = email,
                        user = user,
                        academicYear = academicYear
                    )
                    st.save()
                    return redirect('dashboard')
            except ValidationError as v:
                data['error'] = '\n'.join(v)
                return render(request, 'panel/registerStudent.html', data)
        return render(request,'panel/registerStudent.html', data)


def logoutApp(request):
    logout(request)
    return redirect(login)