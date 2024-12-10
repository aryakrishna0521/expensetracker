from django import forms

from django.contrib.auth.forms import UserCreationForm

from tracker.models import User,ExpenseTracker

class SignUpForm(UserCreationForm):

    class Meta:

        model=User

        fields=["username","email","phone","password1","password2"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "password1":forms.TextInput(attrs={"class":"form-control"}),
            "password2":forms.TextInput(attrs={"class":"form-control"}),
            "phone":forms.NumberInput(attrs={"class":"form-control"}),
            
                 }      


class SignInForm(forms.Form):

    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))

    password=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))


class ExpenseForm(forms.ModelForm):

    class Meta:

        model=ExpenseTracker 

        fields=["title","category","Amount","payment_method"]

        widgets={
                "title":forms.TextInput(attrs={"class":"form-control"}),
                "category":forms.Select(attrs={"class":"form-control form-select"}),
                "Amount":forms.TextInput(attrs={"class":"form-control"}),
                "payment_method":forms.Select(attrs={"class":"form-control form-select"}),



        }


