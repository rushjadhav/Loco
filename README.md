# SetUp

Virtual Environment

    1. Create virtual env
        virtualenv loco_assignment_env

    2. Activate virtual env
        source loco_assignment_env/bin/activate

    3. Install requirements
        pip install -r docs/requirements.txt

Run Test Cases

    python manage.py test

Run Server

    python manage.py runserver

In Memory Database Configuration in settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    }

APIS

    1. POST -/transactionservice/transaction/transaction_id
        payload = { "amount": 5000, "type":"cars" }
        response = { "status": "ok" }

    2. GET /transactionservice/transaction/transaction_id
        response = { "amount": 20.0, "type": test, "parent_id": 1212}

    2. GET /transactionservice/types/cars
        response = [1212, 3434]

    3. GET /transactionservice/sum/10
        response = {"sum":15000}