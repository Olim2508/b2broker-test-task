from django.db import models


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=36, decimal_places=18, default=0)

    def __str__(self):
        return self.label

    def update_balance(self):
        self.balance = (
            self.transactions.aggregate(total=models.Sum("amount"))["total"] or 0
        )
        self.save()


class Transaction(models.Model):
    wallet = models.ForeignKey(
        Wallet, related_name="transactions", on_delete=models.CASCADE
    )
    txid = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=36, decimal_places=18)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.wallet.update_balance()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.wallet.update_balance()

    def __str__(self):
        return self.txid
