from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """
    Paginación global para todos los endpoints de la API.
    - Por defecto: 10 resultados por página.
    - Se puede sobreescribir con ?page_size=XX.
    - Máximo permitido: 100 resultados por página.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
