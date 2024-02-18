from rest_framework.pagination import PageNumberPagination
from api.constants import PAGINATION


class PagePagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGINATION
