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

    model_class = model.__class__

    return model_class, queryset


def _get_model(values):
    if isinstance(values, (QuerySet, list)):
        model = values[0]
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
def knockout_data(values):
    model_class, queryset = _get_model_queryset(values)

    return ko.ko_data(model_class, queryset)


@register.filter
def knockout_view_model(values):
    _, model_class = _get_model(values)

    return ko.ko_view_model(model_class)


@register.filter
def knockout_bindings(values, args=None):
    _, model_class = _get_model(values)

    if not args:
        element_id = None
        ignore_data = False
    else:
        if ',' in args:
            args = args.split(',')
            element_id = args[0]
            if args[1] == 'ignore_data':
                ignore_data = True
            else:
                raise Exception('Unknown argument.')
        else:
            element_id = args
            ignore_data = False

    return ko.ko_bindings(model_class, element_id, ignore_data)


@register.filter
def knockout_model(values):
    model, _ = _get_model(values)

    return ko.ko_model(model)


@register.filter
def knockout_list(values):
    model, _ = _get_model(values)

    return ko.ko_list(model)


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
