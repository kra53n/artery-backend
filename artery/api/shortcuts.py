from django.http import JsonResponse


def json_response(ok: bool, info=None) -> JsonResponse:
    return JsonResponse({'ok': ok, 'info': info} if info else {'ok': ok})