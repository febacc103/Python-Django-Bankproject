import django_filters
from .models import Transactions





class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model=Transactions
        fields=["date","amount","from_account_number","to_account_number","date","amount"]