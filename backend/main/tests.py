from decimal import Decimal

from django.test import tag
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Transaction, Wallet


@tag("transaction")
class TransactionTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.wallet_1 = Wallet.objects.create(label="Wallet 1")
        cls.wallet_2 = Wallet.objects.create(label="Wallet 2")

    def setUp(self):
        self.wallet_1.refresh_from_db()
        self.wallet_2.refresh_from_db()

    def test_get_list_transactions_ordering(self):
        Transaction.objects.create(
            wallet=self.wallet_1, txid="txid_2", amount=Decimal("50.0")
        )
        Transaction.objects.create(
            wallet=self.wallet_1, txid="txid_1", amount=Decimal("20.0")
        )
        Transaction.objects.create(
            wallet=self.wallet_2, txid="txid_3", amount=Decimal("30.0")
        )

        url = reverse_lazy("main:transaction-list")
        response = self.client.get(url, {"ordering": "txid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        txids = [tx["txid"] for tx in response.data["results"]]
        self.assertEqual(txids, ["txid_1", "txid_2", "txid_3"])

        response = self.client.get(url, {"ordering": "-txid"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        txids = [tx["txid"] for tx in response.data["results"]]
        self.assertEqual(txids, ["txid_3", "txid_2", "txid_1"])

        response = self.client.get(url, {"ordering": "amount"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        amounts = [
            Decimal(tx["amount"]).quantize(Decimal("1.0"))
            for tx in response.data["results"]
        ]
        self.assertEqual(amounts, [Decimal("20.0"), Decimal("30.0"), Decimal("50.0")])

    def test_get_list_transactions_filtering(self):
        Transaction.objects.create(
            wallet=self.wallet_1, txid="txid_1", amount=Decimal("20.0")
        )
        Transaction.objects.create(
            wallet=self.wallet_1, txid="txid_2", amount=Decimal("50.0")
        )
        Transaction.objects.create(
            wallet=self.wallet_2, txid="txid_3", amount=Decimal("30.0")
        )

        url = reverse_lazy("main:transaction-list")
        response = self.client.get(url, {"wallet": self.wallet_1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        txids = [tx["txid"] for tx in response.data["results"]]
        self.assertEqual(txids, ["txid_1", "txid_2"])

        response = self.client.get(url, {"wallet": self.wallet_2.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        txids = [tx["txid"] for tx in response.data["results"]]
        self.assertEqual(txids, ["txid_3"])

    def test_create_transaction_updates_wallet_balance(self):
        initial_balance = self.wallet_1.balance
        url = reverse_lazy("main:transaction-list")
        data = {
            "wallet": self.wallet_1.id,
            "txid": "txid_4",
            "amount": "100.0",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.wallet_1.refresh_from_db()
        self.assertEqual(self.wallet_1.balance, initial_balance + Decimal("100.0"))

    def test_create_transaction_with_negative_balance(self):
        url = reverse_lazy("main:transaction-list")
        data = {
            "wallet": self.wallet_1.id,
            "txid": "txid_5",
            "amount": "-100.0",
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_400_BAD_REQUEST, response.data
        )
        self.assertEqual(
            response.json()["non_field_errors"],
            ["Transaction would make wallet balance negative."],
        )
