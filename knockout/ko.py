import cgi
import json
import datetime

from django.template.loader import render_to_string
from django.db.models.fields import related


def _get_knockout_fields(model):
    knockout_fields = model.knockout_fields()
    fields = []
    for knockout_field in knockout_fields:
        fields.append(model._meta.get_field(knockout_field))

    return fields


def _get_relation_dict(field):
    model = field.rel.to
    field_dict = _get_fields(model)
    fields = field_dict['fields']
    fk_fields = field_dict['fks']
    m2m_fields = field_dict['m2ms']

    return {
        'field_name': field.name, 'model': model,
        'nested': {
            'fields': fields,
            'fks': fk_fields,
            'm2ms': m2m_fields
        }
    }


def _get_fields(model, follow_fks=True, follow_m2ms=True):
    '''
    Returns
        {
            'm2ms': [
                {
                    'field_name': <m2m field name>,
                    'model': <m2m field rel to>,
                    'nested': {
                        'm2ms': [<m2m field rel to's m2m>],
                        'fks': [<m2m field rel to's fk>],
                        'fields': [<m2m field rel to's field>]
                    }
                }
            ],
            'fks': [
                {
                    'field_name': <fk field name>,
                    'model': <fk field rel to>,
                    'nested': {
                        'm2ms': [<fk field rel to's m2m>],
                        'fks': [<fk field rel to's fk>],
                        'fields': [<fk field rel to's field>]
                    }
                }
            ],
            'fields': [<field name>],
        }
    '''
    if hasattr(model, 'knockout_fields'):
        model_fields = _get_knockout_fields(model)
    else:
        model_fields = model._meta.get_fields()

    fields = []
    fks = []  # Foreign Keys
    m2ms = []  # Many to Manys
    for field in model_fields:
        if follow_fks and isinstance(field, related.ForeignKey):
            relation_dict = _get_relation_dict(field)
            fks.append(relation_dict)
        elif follow_m2ms and isinstance(field, related.ManyToManyField):
            relation_dict = _get_relation_dict(field)
            m2ms.append(relation_dict)
        elif isinstance(field, (related.ManyToOneRel, related.ManyToManyRel)):
            continue
        else:
            fields.append(field.name)

    return {'fields': fields, 'fks': fks, 'm2ms': m2ms}


def ko_list(model):
    if hasattr(model, "comparator"):
        comparator = str(model.comparator())
    else:
        comparator = 'id'

    model_name = model.__name__
    model_arg = model_name.lower()
    model_args = model_name.lower() + "s"

    list_string = render_to_string(
        "knockout/list.js",
        {'model_name': model_name,
         'comparator': comparator,
         'model_arg': model_arg,
         'model_args': model_args}
    )

    return list_string


def ko_model(model, all_fields=None):
    if not all_fields:
        all_fields = _get_fields(model)
    fields = all_fields['fields']
    fk_fields = all_fields['fks']
    m2m_fields = all_fields['m2ms']

    model_name = model.__name__
    model_arg = model_name.lower()
    model_args = model_name.lower() + "s"

    for field_dict in fk_fields:
        nested = field_dict['nested']
        fk_model = field_dict['model']
        field_dict['model_string'] = ko_model(fk_model, nested)
        field_dict['model_name'] = fk_model.__name__

    for field_dict in m2m_fields:
        nested = field_dict['nested']
        m2m_model = field_dict['model']
        field_dict['model_string'] = ko_model(m2m_model, nested)
        field_dict['model_list'] = ko_list(m2m_model)

    model_string = render_to_string(
        "knockout/model.js",
        {'model_name': model_name,
         'model_arg': model_arg,
         'model_args': model_args,
         'fields': fields,
         'fk_fields': fk_fields,
         'm2m_fields': m2m_fields}
    )

    return model_string


def ko_view_model(model, all_fields=None):
    if not all_fields:
        all_fields = _get_fields(model)

    model_name = model.__name__
    view_model_string = model_name + "ViewModel"

    model_list_string = ko_list(model)
    model_string = ko_model(model, all_fields)

    view_model_string = render_to_string(
        "knockout/view_model.js",
        {'view_model_string': view_model_string,
         'model_list_string': model_list_string,
         'model_string': model_string}
    )

    return view_model_string


def ko_bindings(model, element_id=None):
    model_name = model.__name__
    view_model_string = model_name + "ViewModel"
    model_data_string = model_name + "Data"

    model_bindings_string = render_to_string(
        "knockout/bindings.js",
        {'view_model_string': view_model_string,
         'model_data_string': model_data_string,
         'element_id': element_id}
    )

    return model_bindings_string


def _model_data(obj, fields, safe):
    obj_dict = {}
    for field in fields:
        if hasattr(obj, field):
            attribute = getattr(obj, field)
            if not safe and isinstance(attribute, str):
                attribute = cgi.escape(attribute)
            obj_dict[field] = attribute
        else:
            obj_dict[field] = None

    return obj_dict


def _model_foreign_key_data(obj, fields, safe):
    foreign_key_dict = {}
    for field in fields:
        field_name = field['field_name']
        if hasattr(obj, field_name):
            field_obj = getattr(obj, field_name)
        else:
            field_obj = None

        all_dict = {}
        if field['nested']['fields']:
            foreign_key_obj_dict = _model_data(
                field_obj, field['nested']['fields'], safe
            )
            all_dict.update(foreign_key_obj_dict)

        if field['nested']['fks']:
            nested_foreign_key_obj_dict = _model_foreign_key_data(
                field_obj, field['nested']['fks'], safe
            )
            all_dict.update(nested_foreign_key_obj_dict)

        if field['nested']['m2ms']:
            nested_many_to_many_obj_dict = _model_many_to_many_data(
                field_obj, field['nested']['m2ms'], safe
            )
            all_dict.update(nested_many_to_many_obj_dict)

        foreign_key_dict[field_name] = all_dict

    return foreign_key_dict


def _model_many_to_many_data(obj, fields, safe):
    many_to_many_dict = {}
    for field in fields:
        field_name = field['field_name']
        attribute_list = getattr(obj, field_name)
        many_to_many_obj_list = []
        for attribute in attribute_list.all():
            all_dict = {}

            if field['nested']['fields']:
                many_to_many_obj_dict = _model_data(
                    attribute, field['nested']['fields'], safe
                )
                all_dict.update(many_to_many_obj_dict)

            if field['nested']['fks']:
                nested_foreign_key_obj_dict = _model_foreign_key_data(
                    field['model'], field['nested']['fks'], safe
                )
                all_dict.update(nested_foreign_key_obj_dict)

            if field['nested']['m2ms']:
                nested_many_to_many_obj_dict = _model_many_to_many_data(
                    field['model'], field['nested']['m2ms'], safe
                )
                all_dict.update(nested_many_to_many_obj_dict)

            many_to_many_obj_list.append(all_dict)

        many_to_many_dict[field_name] = many_to_many_obj_list

    return many_to_many_dict


def ko_data(model, queryset, all_fields=None, safe=False):
    if not all_fields:
        all_fields = _get_fields(model)
    fields = all_fields['fields']
    fk_fields = all_fields['fks']
    m2m_fields = all_fields['m2ms']

    model_data = []
    for obj in queryset:
        all_dict = {}

        obj_dict = _model_data(obj, fields, safe)
        all_dict.update(obj_dict)

        foreign_key_dict = _model_foreign_key_data(obj, fk_fields, safe)
        all_dict.update(foreign_key_dict)

        many_to_many_dict = _model_many_to_many_data(obj, m2m_fields, safe)
        all_dict.update(many_to_many_dict)

        model_data.append(all_dict)

    model_name = model.__name__
    model_data_string = model_name + "Data"
    model_args = model_name.lower() + "s"

    dthandler = (
        lambda obj:
            obj.isoformat()
            if isinstance(obj, (datetime.datetime, datetime.date))
            else None
    )

    json_data = json.dumps({model_args: model_data}, default=dthandler)

    model_data_string = render_to_string(
        'knockout/data.js',
        {'model_data_string': model_data_string,
         'data': json_data}
    )

    return model_data_string


def ko(model, queryset, all_fields=None):
    if not all_fields:
        all_fields = _get_fields(model)

    ko_data_string = ko_data(model, queryset, all_fields)
    ko_view_model_string = ko_view_model(model, all_fields)
    ko_bindings_string = ko_bindings(model)

    ko_string = ko_data_string + ko_view_model_string + ko_bindings_string

    return ko_string
