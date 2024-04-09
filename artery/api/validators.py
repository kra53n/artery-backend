from django.core.exceptions import ValidationError


def validate_password(value: str):
    value = value.lstrip().rstrip()
    # NOTE: think about password requirements


def validate_phone(value: str):
    value = value.lstrip().rstrip()
    if not value.isdigit():
        raise ValidationError(f'the number({value}) has letters but only digits allowed')
    if len(value) != 11:
        raise ValidationError(f'the number({value}) must have the length with 11 digits')
