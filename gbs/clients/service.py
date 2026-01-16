from django.http import JsonResponse

def api_error(message, status=400):
    return JsonResponse({
        "success": False,
        "error": message
    }, status=status)


def api_method_not_allowed(message="Méthode non autorisée"):
    return JsonResponse({
        "success": False,
        "error": message
    }, status=405)
