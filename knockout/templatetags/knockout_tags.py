from django import template
from django.db.models import query

from knockout import ko


register = template.Library()


def _get_model_queryset(values):
    if isinstance(values, list):
        queryset = values
        model = values[0]
    elif isinstance(values, query.QuerySet):
        queryset = values
        model = values.model
    else:
        queryset = [values]
        model = values

    model_class = model.__class__

    return model_class, queryset


def _get_model(values):
    if isinstance(values, list):
        model = values[0]
    elif isinstance(values, query.QuerySet):
        model = values.model
    else:
        model = values

    model_class = model.__class__

    return model, model_class


# Accepts a QuerySet, list of objects, instance of a model, or a model class
@register.filter
def knockout(values, ignore_queryset=None):
    if not values:
        raise Exception("Templatetag knockout requires an argument.")

    model_class, queryset = _get_model_queryset(values)

    if ignore_queryset == 'ignore_queryset':
        template = ko.ko(model_class, None)
    else:
        template = ko.ko(model_class, queryset)

    return template


@register.filter
def knockout_data(values, data_variable=None):
    model_class, queryset = _get_model_queryset(values)

    data = ko.ko_data(model_class, queryset, data_variable=data_variable)

    return data


@register.simple_tag
def knockout_view_model(
    values, follow_fks=False, follow_m2ms=False, follow_reverse_fks=False
        ):
    _, model_class = _get_model(values)

    view_model = ko.ko_view_model(
        model_class, None, follow_fks, follow_m2ms, follow_reverse_fks
    )

    return view_model


@register.simple_tag
def knockout_bindings(values, element_id=None, data_variable=None,
                      ignore_data=False):
    _, model_class = _get_model(values)

    bindings = ko.ko_bindings(
        model_class, element_id=element_id,
        data_variable=data_variable, ignore_data=ignore_data
    )

    return bindings


@register.filter
def knockout_model(values):
    model, _ = _get_model(values)

    ko_model = ko.ko_model(model)

    return ko_model


@register.filter
def knockout_list(values):
    model, _ = _get_model(values)

    ko_list = ko.ko_list(model)

    return ko_list


# Helper templatetag, builds up html attributes
@register.assignment_tag
def data_bind(field, template=""):
    data_bind = "data-bind: "

    if template != 'template':
        data_bind += "init, "

    if field.field.widget.__class__.__name__ in ['CheckboxInput']:
        data_bind += "click: $root.clickChecked, checked: "
    else:
        data_bind += "value: "

    data_bind += field.name

    return data_bind
