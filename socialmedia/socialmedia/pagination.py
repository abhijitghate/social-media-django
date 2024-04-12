from rest_framework.pagination import CursorPagination


class CustomPaginationClass(CursorPagination):
    page_size = 10
