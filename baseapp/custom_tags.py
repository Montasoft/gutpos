# En algún archivo de tu proyecto, por ejemplo, `templatetags/custom_tags.py`
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
