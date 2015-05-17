import cgi
import json
import datetime

from django.template.loader import render_to_string


def get_fields(model):
    if hasattr(model, "knockout_fields"):
        fields = model.knockout_fields()
    else:
        fields = []
        for field in model._meta.fields:
            fields.append(field.name)

    return fields


def ko_model(model, fields=None):
    if not fields:
        fields = get_fields(model)

    if hasattr(model, "comparator"):
        comparator = str(model.comparator())
    else:
        comparator = 'id'

    model_name = model.__class__.__name__
    view_model_string = model_name + "ViewModel"
    model_arg = model_name.lower()
    model_args = model_name.lower() + "s"

    model_view_string = render_to_string(
        "knockout/model.js",
        {'model_name': model_name,
         'fields': fields,
         'comparator': comparator,
         'view_model_string': view_model_string,
         'model_arg': model_arg,
         'model_args': model_args}
    )

    return model_view_string


def ko_bindings(model):
    model_name = model.__class__.__name__
    view_model_string = model_name + "ViewModel"
    model_data_string = model_name + "Data"

    model_bindings_string = render_to_string(
        "knockout/bindings.js",
        {'view_model_string': view_model_string,
         'model_data_string': model_data_string}
    )

    return model_bindings_string


def _model_data(obj, fields):
    temp_dict = {}
    for field in fields:
        attribute = getattr(obj, field)
        if isinstance(attribute, str):
            attribute = cgi.escape(attribute)
        temp_dict[field] = attribute

    return temp_dict


def ko_data(model, queryset, fields=None):
    if not fields:
        fields = get_fields(model)

    model_data = []
    for obj in queryset:
        temp_dict = _model_data(obj, fields)
        model_data.append(temp_dict)

    model_name = model.__class__.__name__
    model_data_string = model_name + "Data"

    dthandler = (
        lambda obj:
            obj.isoformat()
            if isinstance(obj, datetime.datetime)
                or isinstance(obj, datetime.date)
            else None
    )

    model_data_string = render_to_string(
        'knockout/data.js',
        {'model_data_string': model_data_string,
         'data': json.dumps(model_data, default=dthandler)
         }
    )

    return model_data_string


def ko(model, queryset, fields=None):
    if not fields:
        fields = get_fields(model)

    ko_data_string = ko_data(model, queryset, fields)
    ko_model_string = ko_model(model, fields)
    ko_bindings_string = ko_bindings(model)

    ko_string = ko_data_string + ko_model_string + ko_bindings_string

    return ko_string
