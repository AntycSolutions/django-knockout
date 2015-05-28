from knockout import ko

from django.db.models.query import QuerySet
from django import template
register = template.Library()


def _get_model_queryset(values):
    if isinstance(values, (QuerySet, list)):
        queryset = values
        model = values[0]
    else:
        queryset = [values]
        model = values

    return model, queryset


def _get_model(values):
    if isinstance(values, (QuerySet, list)):
        model = values[0]
    else:
        model = values

    return model


@register.filter
def knockout(values):
    model, queryset = _get_model_queryset(values)

    model_class = model.__class__

    return ko.ko(model_class, queryset)


@register.filter
def knockout_data(values):
    model, queryset = _get_model_queryset(values)

    model_class = model.__class__

    return ko.ko_data(model_class, queryset,)


@register.filter
def knockout_view_model(values):
    model = _get_model(values)

    model_class = model.__class__

    return ko.ko_view_model(model_class)


@register.filter
def knockout_bindings(values):
    model = _get_model(values)

    model_class = model.__class__

    return ko.ko_bindings(model_class)


@register.filter
def knockout_model(values):
    model = _get_model(values)

    return ko.ko_model(model)


@register.filter
def knockout_list(values):
    model = _get_model(values)

    return ko.ko_list(model)
