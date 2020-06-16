from rest_framework import pagination

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 9 # change the records per page from here

    page_size_query_param = 'page_size'