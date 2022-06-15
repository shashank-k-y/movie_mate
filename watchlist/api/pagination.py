from rest_framework import pagination


class WatchListPagination(pagination.PageNumberPagination):
    page_size = 2


class WatchListLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 3
    max_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'start'
