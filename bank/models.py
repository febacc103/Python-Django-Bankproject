from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser



class MyUser(AbstractUser):
    account_number=models.CharField(max_length=16,unique=True)
    options=(
        ("savings","savings"),
        ("current","current"),
        ("credit","credit")
    )
    account_type=models.CharField(max_length=12,choices=options,default="savings")
    balance=models.FloatField()
    phone=models.CharField(max_length=12)


class Transactions(models.Model):
    from_account_number=models.CharField(max_length=16)
    to_account_number=models.CharField(max_length=16)

    amount=models.FloatField()
    notes=models.CharField(max_length=120)
    date=models.DateField(auto_now=True)
