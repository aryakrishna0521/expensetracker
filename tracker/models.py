from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    phone=models.CharField(max_length=15,unique=True)

class ExpenseTracker(models.Model):

    title=models.CharField(max_length=100) 

    EXPENSE_CATEGORIES = (
    ('Housing', 'Housing'),
    ('Transportation', 'Transportation'),
    ('Food', 'Food'),
    ('Healthcare', 'Healthcare'),
    ('Education', 'Education'),
    ('Entertainment', 'Entertainment'),
    ('Personal Care', 'Personal Care'),
    ('Debt Payments', 'Debt Payments'),
    ('Savings & Investments', 'Savings & Investments'),
    ('Gifts & Donations', 'Gifts & Donations'),
    ('Insurance', 'Insurance'),
    ('Travel', 'Travel'),
    ('Miscellaneous', 'Miscellaneous'),
)

    category=models.CharField(max_length=100,choices=EXPENSE_CATEGORIES,default="Food")

    Amount=models.PositiveIntegerField()

    payment_options=(
        ("card","card"),
        ("cash","cash"),
        ("UPI","UPI")
    )

    payment_method=models.CharField(max_length=100,choices=payment_options,default="cash")
    owner=models.ForeignKey(User,on_delete=models.CASCADE, )


    def __str__(self):
        return self.title


