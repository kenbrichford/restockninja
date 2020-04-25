from django import template

register = template.Library()

@register.filter
def dollars(cents):
    return '${:.2f}'.format(cents / 100)