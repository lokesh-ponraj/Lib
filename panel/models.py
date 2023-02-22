from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    fullName = models.CharField(max_length=200, null=True)
    rollNo = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    balance = models.DecimalField(decimal_places=2,max_digits=7,default=0.0)
    academicYear = models.CharField(max_length=200,
    choices= (
        ('I year', 'I year'),
        ('II year', 'II year'),
        ('III year', 'III year'),
        ('IV year', 'IV year')
    )
    )

    def __str__(self):
        return self.fullName


class Book(models.Model):
    isbn_num = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    copies = models.IntegerField(null=True)


    def __str__(self):
        return self.title

class Borrow(models.Model):
    borrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowedOn = models.DateField(auto_now_add=True)
    dueDate = models.DateField(null=True)
    fineAmount = models.DecimalField(decimal_places=2,max_digits=7, default=0.0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)


    def __str__(self):
        return str(self.borrower)+"-"+str(self.book)


class Transaction(models.Model):
    id = models.CharField(primary_key=True, unique=True, default=uuid.uuid4, max_length=256)
    payment_timestamp = models.DateTimeField(auto_now_add=True)
    payer = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Book, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(decimal_places=2, max_digits=7, default=0.0)


    def __str__(self):
        return id


# @receiver(post_save, sender=Student)
# def createUser(sender, instance, **kwargs):
#     if instance.user == None:
#         fullName = instance.fullName.split(' ')
#         firstName, lastName = fullName[0], ''.join(fullName[1:])
#         user = User.objects.create_user(''.join(fullName[:10]).lower(), instance.email, 'Pass@2022')
#         user.first_name = firstName
#         user.last_name = lastName
#         user.save()
#         stud = Student.objects.get(id = instance.id)
#         stud.user = user
#         stud.save()