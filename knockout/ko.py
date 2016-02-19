import inspect

from django.template.loader import render_to_string


def ko_list(model_class):
    if not inspect.isclass(model_class):
        raise Exception('ko_list function requires a class')

    if hasattr(model_class, "comparator"):
        comparator = str(model_class.comparator())
    else:
        comparator = 'id'

    model_name = model_class.__name__
    model_arg = model_name.lower()
    model_args = model_name.lower() + "s"

    list_string = render_to_string(
        "knockout/list.js",
        {
            'model_name': model_name,
            'comparator': comparator,
            'model_arg': model_arg,
            'model_args': model_args,
        }
    )

    return list_string


def ko_model(model_class):
    if not inspect.isclass(model_class):
        raise Exception('ko_model function requires a class')

    model_name = model_class.__name__
    model_arg = model_name.lower()
    model_args = model_name.lower() + "s"

    model_string = render_to_string(
        "knockout/model.js",
        {
            'model_name': model_name,
            'model_arg': model_arg,
            'model_args': model_args,
        }
    )

    return model_string


def ko_view_model(model_class,):
    if not inspect.isclass(model_class):
        raise Exception('ko_view_model function requires a class')

    model_name = model_class.__name__
    view_model_string = model_name + "ViewModel"

    model_list_string = ko_list(model_class)
    model_string = ko_model(model_class)

    view_model_string = render_to_string(
        "knockout/view_model.js",
        {
            'view_model_string': view_model_string,
            'model_list_string': model_list_string,
            'model_string': model_string,
        }
    )

    return view_model_string


def ko_bindings(model_class, element_id=None):
    if not inspect.isclass(model_class):
        raise Exception('ko_bindings function requires a class')

    model_name = model_class.__name__
    view_model_string = model_name + "ViewModel"

    model_bindings_string = render_to_string(
        "knockout/bindings.js",
        {
            'view_model_string': view_model_string,
            'element_id': element_id,
        }
    )

    return model_bindings_string


def ko(model_class):
    if not inspect.isclass(model_class):
        raise Exception('ko function requires a class')

    ko_view_model_string = ko_view_model(model_class)
    ko_bindings_string = ko_bindings(model_class)

    ko_string = ko_view_model_string + ko_bindings_string

    return ko_string
