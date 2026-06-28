from django.http import JsonResponse


def handler404(request, exception=None):
    return JsonResponse(
        {'error': 'Not Found', 'detail': 'La ruta solicitada no existe.'},
        status=404,
    )


def handler500(request):
    return JsonResponse(
        {'error': 'Internal Server Error', 'detail': 'Ocurrió un error interno en el servidor.'},
        status=500,
    )
