from django import template

register = template.Library()


@register.filter(name='split')
def split(value, sep=','):
    """Split a string by `sep` and return list. Safe for None.

    Usage in template: `mystring|split:","`
    """
    if value is None:
        return []
    try:
        return [part.strip() for part in value.split(sep) if part.strip()]
    except Exception:
        return []
from django import template

register = template.Library()


@register.filter(name='split')
def split(value, sep=','):
    """Split a string by `sep` and return list. Safe for None.

    Usage in template: `mystring|split:","`
    """
    if value is None:
        return []
    try:
        return [part.strip() for part in value.split(sep) if part.strip()]
    except Exception:
        return []
