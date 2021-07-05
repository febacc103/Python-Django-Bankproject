from django.shortcuts import render,redirect
from .forms import AccountCreationForm
from django.views.generic import CreateView,TemplateView
from .models import MyUser,Transactions
from django.urls import reverse_lazy
from .forms import LoginForm,TransactionForm
from django.contrib.auth import authenticate,login,logout
from .decorators import loginrequired
from django.utils.decorators import method_decorator
from .filters import TransactionFilter
from django.db.models import Q



# Create your views here.


class AccountCreateView(CreateView):
    model = MyUser
    form_class = AccountCreationForm
    template_name ="account_create.html"
    success_url =reverse_lazy("signin")


class SigninView(TemplateView):
    model=MyUser
    form_class=LoginForm
    template_name = ("login.html")
    context= {}
    def get(self, request, *args, **kwargs):
        form=self.form_class()
        self.context["form"]=form
        return render(request,self.template_name,self.context)
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                print("succ")
                login(request,user)
                return redirect("home")
            else:
                print("fail")
        return render(request,self.template_name,self.context)


@method_decorator(loginrequired,name="dispatch")
class BalanceView(TemplateView):
    template_name = "home.html"
    context={}
    def get(self, request, *args, **kwargs):
        balance=request.user.balance
        print(balance)
        self.context["balance"]=balance
        return render(request,self.template_name,self.context)



class GetUserAccountMixin():
    def get_user_account(self,acc_no):
        try:
            return MyUser.objects.get(account_number=acc_no)
        except:
            return None


def sign_out(request, *args, **kwargs):
    logout(request)
    return redirect("signin")



@method_decorator(loginrequired,name="dispatch")
class FundTransferView(TemplateView,GetUserAccountMixin):
    model=Transactions
    form_class=TransactionForm
    template_name = "fund_transfer.html"
    context={}
    def get(self, request, *args, **kwargs):
        self.context["form"] = self.form_class(initial={'from_account_number':request.user.account_number})
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            faccount_number=request.user.account_number
            taccount_number=form.cleaned_data.get("confirm_account_number")
            amount=form.cleaned_data.get("amount")
            notes=form.cleaned_data.get("notes")
            transaction=Transactions(from_account_number=faccount_number,
                                     to_account_number=taccount_number,
                                     amount=amount,
                                     notes=notes)
            transaction.save()
            user=self.get_user_account(faccount_number)
            user.balance-=amount
            user.save()
            user = self.get_user_account(taccount_number)
            user.balance += amount
            user.save()
            return redirect("home")
        else:
            form=self.form_class(request.POST)
            self.context["form"] = form
            return render(request, self.template_name, self.context)




@method_decorator(loginrequired,name="dispatch")
class PaymentHistory(TemplateView):
    model=Transactions
    template_name = "paymenthistory.html"
    context={}
    def get(self, request, *args, **kwargs):
        ctransactions=self.model.objects.filter(to_account_number=request.user.account_number)
        dtransactions=self.model.objects.filter(from_account_number=request.user.account_number)
        self.context["ctransactions"]=ctransactions
        self.context["dtransactions"]=dtransactions
        return render(request,self.template_name,self.context)






class TransactionFilterView(TemplateView):
    def get(self, request, *args, **kwargs):
        transactions=Transactions.objects.filter(Q(to_account_number=request.user.account_number)|Q(from_account_number=request.user.account_number))
        transaction_filter=TransactionFilter(request.GET,queryset=transactions)
        return render(request,"filterhistory.html",{'filter':transaction_filter})

