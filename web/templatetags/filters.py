# Thanks to maciek and Charlesthk for the below: https://stackoverflow.com/a/18962676

from django import template

register = template.Library()

# adds a class, eg. to a form field
@register.filter(name="addclass")
def addclass(value, name):
    return value.as_widget(attrs={"class": name})
