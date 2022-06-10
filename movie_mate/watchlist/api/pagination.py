from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)


class WatchListPagination(PageNumberPagination):
    page_size = 2


class WatchListLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
