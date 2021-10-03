from django import template

register = template.Library()


@register.filter(name="remainder")
def remainder(n):
    return (n % 3)