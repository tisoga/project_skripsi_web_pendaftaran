from django import template
register = template.Library()

@register.filter
def pembagian_kuota(value):
    return int(value) + 1