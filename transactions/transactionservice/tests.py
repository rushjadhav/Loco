from django.test import Client
from django.test import TestCase
from transactionservice.models import Transaction


class BaseTestClass(TestCase):
    """
    Base class to create required data for testing
    """

    def setUp(self):
        transaction = Transaction.objects.create(amount=10.0, type="test", transaction_id=123)
        Transaction.objects.create(amount=20.0, type="test", transaction_id=1234,
                                   parent=transaction)
        Transaction.objects.create(amount=20.0, type="test", transaction_id=12345,
                                   parent=transaction)

    def tearDown(self):
        Transaction.objects.all().delete()


class TransactionTestCase(BaseTestClass):
    """
    Unit test class for testing transaction model
    """

    def test_get_total_amount_without_child_transaction(self):

        transaction = Transaction.objects.get(transaction_id=12345)
        self.assertEquals(transaction.get_total_amount(), 20.0)

    def test_get_total_amount_with_child_transaction(self):

        transaction = Transaction.objects.get(transaction_id=123)
        self.assertEquals(transaction.get_total_amount(), 50.0)


class TestTransactionView(BaseTestClass):
    """
    Unit test class for testing transaction api
    """

    def test_get_method_with_invalid_transaction_id(self):
        client = Client()
        response = client.get('/transactionservice/transaction/1234544545454545/')
        self.assertEquals(response.status_code, 404)

    def test_get_method_with_valid_transaction_id(self):
        client = Client()
        response = client.get('/transactionservice/transaction/1234/')
        self.assertEquals(response.status_code, 200)

    def test_get_method_for_transaction_data(self):
        client = Client()
        response = client.get('/transactionservice/transaction/1234/')
        self.assertContains(response, 20.0)
        self.assertContains(response, "test")

    def test_post_method_with_invalid_input(self):
        client = Client()
        response = client.post('/transactionservice/transaction/1212/', {'amount': 'test', 'type': 'test'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "value must be a decimal number")

    def test_post_method_for_unique_transaction_id(self):
        client = Client()
        response = client.post('/transactionservice/transaction/1234/', {'amount': 10.0, 'type': 'test'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Transaction with this Transaction id already exists")

    def test_post_method_with_valid_input(self):
        client = Client()
        response = client.post('/transactionservice/transaction/34343434/', {'amount': 10.0, 'type': 'test'})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "OK")


class TestGetTransactionsByTypeView(BaseTestClass):
    """
    Unit test class for testing GetTransactionsByType View
    """

    def test_get_method_with_valid_transaction_type(self):
        client = Client()
        response = client.get('/transactionservice/types/test/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 123)

    def test_get_method_with_invalid_transaction_type(self):
        client = Client()
        response = client.get('/transactionservice/types/invalid/')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, '[]')


class TestGetTransactionSumView(BaseTestClass):
    """
    Unit test class for testing GetTransactionSum View
    """

    def test_get_method_with_valid_transaction_id(self):
        client = Client()
        response = client.get('/transactionservice/sum/1234/')
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 20.0)

    def test_get_method_with_invalid_transaction_id(self):
        client = Client()
        response = client.get('/transactionservice/sum/6666655555/')
        self.assertEquals(response.status_code, 404)