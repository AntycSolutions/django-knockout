# http://vanderwijk.info/blog
# /adding-css-classes-formfields-in-django-templates/

from django import template
register = template.Library()


@register.filter
def add_css(field, css):
    attrs = {}
    definition = css.split('|')
    for d in definition:
        if ':' not in d:
            attrs[d] = True
        else:
            t, v = d.split(':', 1)
            attrs[t] = v.strip()

    return field.as_widget(attrs=attrs)
