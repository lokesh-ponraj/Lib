from django.db import models
from django.contrib.auth.models import User

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
    borrrower = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowedOn = models.DateField(auto_now_add=True)
    dueDate = models.DateField(null=True)
    fineAmount = models.DecimalField(decimal_places=2,max_digits=7, default=0.0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=None)
