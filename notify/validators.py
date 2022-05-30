from django.core.exceptions import ValidationError

from tidylib import tidy_document


def validate_html(value):
    _, errors = tidy_document(
        value,
        options={'numeric-entities': 1, 'show-body-only': 1}
    )

    if errors:
        raise ValidationError(errors)

    return value
