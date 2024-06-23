from decimal import Decimal

from rest_framework import serializers

from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"

    def validate(self, attrs):
        wallet = attrs.get("wallet")
        new_balance = wallet.balance + attrs["amount"]
        if new_balance < Decimal("0"):
            raise serializers.ValidationError(
                "Transaction would make wallet balance negative."
            )
        return attrs
