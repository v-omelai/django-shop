from rest_framework.exceptions import APIException


class TransactionException(APIException):
    status_code = 422
    default_detail = 'Transaction cannot be processed'
    default_code = 'Transaction cannot be processed'
