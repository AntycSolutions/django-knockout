import inspect

from django.template.loader import render_to_string
from django.core import urlresolvers

from knockout import settings


def ko_list(model_class):
    if not inspect.isclass(model_class):
        raise Exception('ko_list function requires a class')

    if hasattr(model_class, "comparator"):
        comparator = str(model_class.comparator())
    else:
        comparator = 'id'

    model_name = model_class.__name__
    model_list = model_name.lower() + "s"

    list_string = render_to_string(
        "knockout/list.js",
        {
            'model_name': model_name,
            'comparator': comparator,
            'model_list': model_list,
        }
    )

    return list_string


def _get_url(context, model_name):
    if settings.SETTINGS['disable_ajax_data']:
        return

    app_name = context['request'].resolver_match.app_name
    if not app_name:
        raise Exception('urls app_name is undefined')
    url_name = '{}:{}-list'.format(
        context['request'].resolver_match.app_name, model_name.lower()
    )
    url = urlresolvers.reverse(url_name)

    return url


def ko_view_model(model_class, context=None, url=None):
    if not inspect.isclass(model_class):
        raise Exception('ko_model function requires a class')

    model_name = model_class.__name__
    l_model_name = model_name.lower()
    model_options_var = l_model_name + '_options'
    model_fields_var = l_model_name + '_fields'

    if not url:
        url = _get_url(context, model_name)

    model_string = render_to_string(
        "knockout/model.js",
        {
            'model_name': model_name,
            'model_options_var': model_options_var,
            'model_fields_var': model_fields_var,
            'url': url,
            'ajax_data': not settings.SETTINGS['disable_ajax_data'],
            'ajax_options': not settings.SETTINGS['disable_ajax_options'],
            'jquery': not settings.SETTINGS['disable_jquery'],
        }
    )

    return model_string


def ko_list_view_model(model_class, context=None, url=None):
    if not inspect.isclass(model_class):
        raise Exception('ko_view_model function requires a class')

    model_name = model_class.__name__
    view_model_class = model_name + "ViewModel"

    model_list_string = ko_list(model_class)
    model_string = ko_view_model(model_class, context=context, url=url)

    view_model_string = render_to_string(
        "knockout/view_model.js",
        {
            'view_model_class': view_model_class,
            'model_list_string': model_list_string,
            'model_string': model_string,
        }
    )

    return view_model_string


def ko_bindings(model_class, element_id=None, context=None, url=None):
    if not inspect.isclass(model_class):
        raise Exception('ko_bindings function requires a class')

    model_name = model_class.__name__
    l_model_name = model_name.lower()
    model_list = l_model_name + "s"
    model_options_var = l_model_name + '_options'
    view_model_class = model_name + "ViewModel"
    view_model_object = view_model_class.lower()

    if not url:
        url = _get_url(context, model_name)

    model_bindings_string = render_to_string(
        "knockout/bindings.js",
        {
            'model_list': model_list,
            'model_options_var': model_options_var,
            'view_model_class': view_model_class,
            'view_model_object': view_model_object,
            'element_id': element_id,
            'url': url,
            'ajax_data': not settings.SETTINGS['disable_ajax_data'],
            'ajax_options': not settings.SETTINGS['disable_ajax_options'],
            'jquery': not settings.SETTINGS['disable_jquery'],
        }
    )

    return model_bindings_string


def ko(model_class, context=None, url=None):
    if not inspect.isclass(model_class):
        raise Exception('ko function requires a class')

    ko_view_model_string = ko_list_view_model(
        model_class, context=context, url=url
    )
    ko_bindings_string = ko_bindings(model_class, context=context, url=url)

    ko_string = ko_view_model_string + ko_bindings_string

    return ko_string
