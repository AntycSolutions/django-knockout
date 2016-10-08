import inspect

from django import template
from django.db.models import query

from knockout import ko, forms


register = template.Library()


def _get_model_class(values):
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
@register.simple_tag(takes_context=True)
def knockout(context, values, url=None):
    if not values and not hasattr(values, 'model'):
        raise Exception("knockout tag requires an argument.")

    model_class = _get_model_class(values)

    template = ko.ko(model_class, context=context, url=url)

    return template


@register.simple_tag(takes_context=True)
def knockout_list_view_model(context, values, url=None):
    if not values and not hasattr(values, 'model'):
        raise Exception("knockout_view_model tag requires an argument.")

    model_class = _get_model_class(values)

    view_model = ko.ko_list_view_model(model_class, context=context, url=url)

    return view_model


@register.simple_tag(takes_context=True)
def knockout_bindings(context, values, element_id=None, url=None):
    if not values and not hasattr(values, 'model'):
        raise Exception("knockout_model tag requires an argument.")

    model_class = _get_model_class(values)

    bindings = ko.ko_bindings(
        model_class, element_id=element_id, context=context, url=url
    )

    return bindings


@register.simple_tag(takes_context=True)
def knockout_view_model(context, values, url=None):
    if not values and not hasattr(values, 'model'):
        raise Exception("knockout_model tag requires an argument.")

    model_class = _get_model_class(values)

    ko_model = ko.ko_view_model(model_class, context=context, url=url)

    return ko_model


@register.simple_tag
def knockout_list(values):
    if not values and not hasattr(values, 'model'):
        raise Exception("knockout_list tag requires an argument.")

    model_class = _get_model_class(values)

    ko_list = ko.ko_list(model_class)

    return ko_list


# Helper tag, renders data-bind attr required by knockout
@register.assignment_tag
def data_bind(field):
    if not field:
        raise Exception("data_bind tag requires an argument.")

    data_bind = "data-bind: "

    attr = forms.render_data_bind_attr(field, field.name)

    return data_bind + attr
