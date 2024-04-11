from django.http import JsonResponse


def json_response(ok: bool, info=None, status: int | None = None) -> JsonResponse:
    if ok:
        status = 200
    else:
        assert status != None
    response = JsonResponse({'ok': ok, 'info': info} if info else {'ok': ok})
    response.status_code = status
    return response