from django.db import models

class TransactionRecord(models.Model):
    tx_id = models.CharField(max_length=200, unique=True)
    sender = models.CharField(max_length=140)
    receiver = models.CharField(max_length=140)
    amount = models.FloatField()
    data = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tx_id}: {self.sender}->{self.receiver} ({self.amount})'