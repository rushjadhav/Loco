from django.conf.urls import url

from transactionservice import views

urlpatterns = [
    url(r'^transaction/(?P<transaction_id>[0-9]+)/$', views.TransactionView.as_view(), name='transaction'),
    url(r'^types/(?P<transaction_type>\w+)/$', views.GetTransactionsByType.as_view(), name='transaction_types'),
    url(r'^sum/(?P<transaction_id>[0-9]+)/$', views.GetTransactionSum.as_view(), name='transaction_sum'),
]
