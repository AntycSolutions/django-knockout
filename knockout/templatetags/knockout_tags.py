import inspect

from django import template
from django.db.models import query

from knockout import ko, forms


register = template.Library()


def get_model_class(values):
    if isinstance(values, list):
        model = values[0]
        model_class = model.__class__
    elif isinstance(values, query.QuerySet):
        model = values.model
        model_class = model
    elif inspect.isclass(values):
        model_class = values
    else:
        model = values
        model_class = model.__class__

    return model_class


# Accepts a QuerySet, list of objects, instance of a model, or a model class
@register.simple_tag
def knockout(values):
    if not values:
        raise Exception("knockout tag requires an argument.")

    model_class = get_model_class(values)

    template = ko.ko(model_class)

    return template


@register.simple_tag
def knockout_view_model(values):
    if not values:
        raise Exception("knockout_view_model tag requires an argument.")

    model_class = get_model_class(values)

    view_model = ko.ko_view_model(model_class)

    return view_model


@register.simple_tag
def knockout_bindings(values, element_id=None):
    if not values:
        raise Exception("knockout_model tag requires an argument.")

    model_class = get_model_class(values)

    bindings = ko.ko_bindings(model_class, element_id=element_id)

    return bindings


@register.simple_tag
def knockout_model(values):
    if not values:
        raise Exception("knockout_model tag requires an argument.")

    model_class = get_model_class(values)

    ko_model = ko.ko_model(model_class)

    return ko_model


@register.simple_tag
def knockout_list(values):
    if not values:
        raise Exception("knockout_list tag requires an argument.")

    model_class = get_model_class(values)

    ko_list = ko.ko_list(model_class)

    return ko_list


# Helper tag, renders data-bind attr
@register.assignment_tag
def data_bind(field):
    if not field:
        raise Exception("data_bind tag requires an argument.")

    data_bind = "data-bind: "

    attr = forms.render_data_bind_attr(field, field.name)

    return data_bind + attr
