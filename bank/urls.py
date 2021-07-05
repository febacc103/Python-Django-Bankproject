from django.urls import path

from .views import AccountCreateView,SigninView,BalanceView,sign_out,FundTransferView,PaymentHistory,TransactionFilterView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns=[
    path("login",SigninView.as_view(),name="signin"),
    path("register",AccountCreateView.as_view(),name="register"),
    path("home",login_required(TemplateView.as_view(template_name="home.html"),login_url="signin"),name="home"),
    path("balance",BalanceView.as_view(),name="balance"),
    path("signout", sign_out, name="logout"),
    path("transactions",FundTransferView.as_view(),name="transaction"),
    path("payment",PaymentHistory.as_view(),name="payment"),
    path("filter",TransactionFilterView.as_view(),name="filter")
]
