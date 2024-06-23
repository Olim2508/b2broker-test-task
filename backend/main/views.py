from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import *
from .serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["label"]
    ordering_fields = ["label", "balance"]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.order_by("id")
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["wallet", "txid", "amount"]
    ordering_fields = ["txid", "amount"]
