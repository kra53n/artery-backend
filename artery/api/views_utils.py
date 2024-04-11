from typing import Iterable

from .shortcuts import json_response


def check_fields(*field_names: Iterable[int]):
    '''
        `@check_fields(field_names)` decorator applyied for methods with
    (self, request) arguments. The output value of `@check_field` will
    be paste to the `method` as the third argument.
        Works only with POST request because GET request can not send any
    forms data.

    Usage example may be seen in artery/api/views.py/CompanyCities class.
    '''
    def decorator(method):
        def wrapper(*args):
            field_vals = []
            request = args[1]
            for field_name in field_names:
                field_val = None
                if field_name in request.session:
                    field_val = request.session[field_name]
                # TODO: delete this block of condition due unsecurity
                elif field_name in request.POST:
                    field_val = request.POST[field_name]
                if not field_val:
                    return json_response(
                        ok=False,
                        info=f'{field_name} was not given',
                        status=400,
                    )
                field_vals.append(field_val)
            return method(*args, *field_vals)
        return wrapper
    return decorator