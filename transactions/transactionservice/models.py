from __future__ import unicode_literals

from django.db import models


class Transaction(models.Model):
    """
    Class representing a transaction
    """

    type = models.CharField(max_length=48, null=False, blank=False)

    amount = models.DecimalField(max_digits=6, decimal_places=2)

    parent = models.ForeignKey("Transaction", related_name='child_transactions', null=True, blank=True)

    transaction_id = models.BigIntegerField(unique=True, null=False, blank=False)

    def get_total_amount(self):
        return self.amount+sum(list(self.child_transactions.all().values_list('amount', flat=True)))

    class Meta:
        db_table = 'transaction'
