from django.shortcuts import render,redirect,get_object_or_404

from django.views import View

from tracker.forms import SignUpForm,SignInForm,ExpenseForm

from tracker.models import ExpenseTracker

# Create your views here.
from django.contrib.auth import authenticate,login,logout

from django.db.models import Q

from django.contrib import messages

from django.utils.decorators import method_decorator

from tracker.decorators import signin_required

from django.views.decorators.cache import never_cache

decs=[signin_required,never_cache]


class SignUpView(View):

    template_name="signup.html"

    form_class=SignUpForm

    def get(self,request,*arg,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            form_instance.save()

            return redirect("signin")

        print("account creation failed")

        return render(request,self.template_name,{"form":form_instance})

class SignInView(View):

    template_name="signin.html"

    form_class=SignInForm


    def get(self,request,*args,**kwargs):

        form_instance=self.form_class()

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST 

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            uname=data.get("username")

            pwd=data.get("password")

            user_obj=authenticate(request,username=uname,password=pwd)

            if user_obj:

                login(request,user_obj)


                return redirect("expense-list")


        return render(request,self.template_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect("signin")

@method_decorator(decs,name="dispatch")
class ExpenseListView(View):
    templte_name="expense_list.html"

    def get(self,request,*args,**kwargs):

        search_text=request.GET.get("filter")

        qs=ExpenseTracker.objects.filter(owner=request.user)

        all_title=ExpenseTracker.objects.values_list("title",flat=True).distinct()

        all_categoryt=ExpenseTracker.objects.values_list("category",flat=True).distinct()

        all_payment_method=ExpenseTracker.objects.values_list("payment_method",flat=True).distinct()

        all_records=[]

        all_records.extend(all_title)

        all_records.extend(all_categoryt)

        all_records.extend(all_payment_method)

        if search_text:

            qs=qs.filter(Q(title__contains=search_text)|Q(category__contains=search_text)|Q(payment_method__contains=search_text))
        
            messages.success(request,"employee list fetched sucessfully")

        return render(request,self.templte_name,{"data":qs,"records":all_records})

@method_decorator(decs,name="dispatch")
class ExpenseAddView(View):
    templte_name="expense_add.html"
    form_class=ExpenseForm

    def get(self,request,*args,**kwargs):
        form_instance=self.form_class

        return render(request,self.templte_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        form_data=request.POST

        form_instance=self.form_class(form_data)

        if form_instance.is_valid():

            data=form_instance.cleaned_data

            ExpenseTracker.objects.create(**data,owner=request.user)

            return redirect("expense-list")

            messages.success(request,"expense added sucessfully")


        messages.error(request,"expense not added ")

        return render(request,self.templte_name,{"form":form_instance})

@method_decorator(decs,name="dispatch")
class ExpenseDetailView(View):

    template_name="expense_detail.html"

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        qs=ExpenseTracker.objects.get(id=id)

        return render(request,self.template_name,{"data":qs})


@method_decorator(decs,name="dispatch")
class ExpenseDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        ExpenseTracker.objects.get(id=id).delete()

        messages.success(request,"expense removed sucessfully")


        return redirect("expense-list")


@method_decorator(decs,name="dispatch")
class ExpenseUpdateView(View):

    template_name="expense_edit.html"

    form_class=ExpenseForm

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=get_object_or_404(ExpenseTracker,id=id)

        form_instance=self.form_class(instance=expense_object)

        return render(request,self.template_name,{"form":form_instance})

    def post(self,request,*args,**kwargs):

        id=kwargs.get("pk")

        expense_object=get_object_or_404(ExpenseTracker,id=id)

        form_data=request.POST

        form_instance=self.form_class(form_data,instance=expense_object)

        if form_instance.is_valid():

            form_instance.save()

            messages.success(request,"expense updated sucessfully")


            return redirect("expense-list")

        messages.success(request,"expense not updated")


        return render(request,self.template_name,{"form":form_instance})

from django.db.models import Sum

class ExpenseSummaryView(View):
    template_name="expense_summary.html"
    def get(self,request,*args,**kwargs):
        qs=ExpenseTracker.objects.filter(owner=request.user)

        total_expense=qs.values("Amount").aggregate(total=Sum("Amount"))
        print(total_expense)

        payment_summary=qs.values("payment_method").annotate(total=Sum("Amount"))
        print(payment_summary)

        category_summary=qs.values("category").annotate(total=Sum("Amount"))
        print(category_summary)

        context={
            "total_expense":total_expense.get("total"),
            "payment_summary":payment_summary,
            "category_summary":category_summary
        }

        return render(request,self.template_name,context)
