from knockout import ko

from django.db.models.query import QuerySet
from django import template
register = template.Library()


@register.filter
def knockout(values):
    if isinstance(values, (QuerySet, list)):
        queryset = values
        model = values[0]
    else:
        queryset = [values]
        model = values

    fields = ko.get_fields(model)

    return ko.ko(model, queryset, fields)


@register.filter
def knockout_data(values):
    if isinstance(values, (QuerySet, list)):
        queryset = values
        model = values[0]
    else:
        queryset = [values]
        model = values

    fields = ko.get_fields(model)

    return ko.ko_data(model, queryset, fields)


@register.filter
def knockout_model(values):
    if isinstance(values, (QuerySet, list)):
        model = values[0]
    else:
        model = values

    fields = ko.get_fields(model)

    return ko.ko_model(model, fields)


@register.filter
def knockout_bindings(values):
    if isinstance(values, (QuerySet, list)):
        model = values[0]
    else:
        model = values

    return ko.ko_bindings(model)
