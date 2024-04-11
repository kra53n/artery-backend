from .shortcuts import json_response


def check_field(field_name: str):
    '''
    `@check_field(field_name)` decorator applyied for methods with
    (self, request) arguments. The output value of `@check_field`
    will be paste to the `method` as the third argument.

    Usage example may be seen in artery/api/views.py/CompanyCities class
    '''
    def decorator(method):
        def wrapper(*args):
            field_val = None
            request = args[1]
            if field_name in request.session:
                field_val = request.session[field_name]
            # TODO: delete this block of condition due unsecurity
            elif field_name in request.POST:
                field_val = request.POST[field_name]
            if field_val:
                return method(*args, field_val)
            return json_response(
                ok=False,
                info=f'{field_name} was not given',
                status=400,
            )
        return wrapper
    return decorator