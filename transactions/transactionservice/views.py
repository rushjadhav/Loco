from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from transactionservice.models import Transaction


class TransactionView(View):

    def get(self, request, transaction_id):

        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        return JsonResponse({'type': transaction.type, 'amount': transaction.amount,
                             'parent_id': transaction.parent_id})

    def post(self, request, transaction_id):
        transaction_type = request.POST.get('type')
        transaction_amount = request.POST.get('amount')
        parent_id = request.POST.get('parent__transaction_id')

        transaction = Transaction(type=transaction_type,amount=transaction_amount,
                                  parent_id=parent_id, transaction_id=transaction_id)
        try:
            transaction.full_clean()
            transaction.save()
            response = {'status': 'OK'}
        except ValidationError as e:
            response = e.message_dict

        return JsonResponse(response)


class GetTransactionsByType(View):

    def get(self, request, transaction_type):
        transaction_ids = Transaction.objects.filter(type=transaction_type).values_list('transaction_id', flat=True)
        return JsonResponse(list(transaction_ids), safe=False)


class GetTransactionSum(View):

    def get(self, request, transaction_id):
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        return JsonResponse({'sum': transaction.get_total_amount()})