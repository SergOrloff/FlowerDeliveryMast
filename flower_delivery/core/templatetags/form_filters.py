# core\admin\templatetags\form_filters.py
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    existing_classes = value.field.widget.attrs.get("class", "")
    new_classes = f"{existing_classes} {css_class}".strip()
    return value.as_widget(attrs={"class": new_classes})

@register.filter(name='add_attrs')
def add_attrs(value, attrs):
    attributes = {}
    for attr in attrs.split(','):
        key, val = attr.split('=')
        attributes[key] = val
    existing_classes = value.field.widget.attrs.get("class", "")
    if "class" in attributes:
        attributes["class"] = f"{existing_classes} {attributes['class']}".strip()
    return value.as_widget(attrs=attributes)
