import inspect

from django.template.loader import render_to_string
from django.core import urlresolvers

from knockout import settings, utils


def ko_list_utils(model_class):
    if not inspect.isclass(model_class):
        raise Exception('ko_list_utils function requires a class')

    if hasattr(model_class, "comparator"):
        comparator = str(model_class.comparator())
    else:
        comparator = 'id'

    model_name = model_class.__name__
    model_list = model_name.lower() + "s"
    view_model_class = model_name + 'ViewModel'

    list_utils_string = render_to_string(
        "knockout/list_utils.js",
        {
            'comparator': comparator,
            'model_list': model_list,
            'view_model_class': view_model_class,
        }
    )

    return list_utils_string


def _get_url(context, model_name):
    if settings.SETTINGS['disable_ajax_data']:
        return

    if not context:
        raise Exception(
            'Please provide full context when not specifying an url'
        )

    app_name = context['request'].resolver_match.app_name
    if not app_name:
        raise Exception('urls app_name is undefined')
    url_name = '{}:{}-list'.format(
        context['request'].resolver_match.app_name, model_name.lower()
    )
    url = urlresolvers.reverse(url_name)

    return url


def ko_view_model(
    model_class, context=None, url=None, disable_ajax_options=False
):
    if not inspect.isclass(model_class):
        raise Exception('ko_model function requires a class')

    model_name = model_class.__name__
    l_model_name = model_name.lower()
    model_options_var = l_model_name + '_options'
    model_fields_var = l_model_name + '_fields'
    view_model_class = model_name + 'ViewModel'
    list_view_model_class = model_name + 'ListViewModel'

    if not url:
        url = _get_url(context, model_name)

    knockout_options = utils.get_knockout_options(model_class, None)

    if not disable_ajax_options:
        ajax_options = not settings.SETTINGS['disable_ajax_options']
    else:
        ajax_options = not disable_ajax_options

    view_model_string = render_to_string(
        "knockout/view_model.js",
        {
            'model_options_var': model_options_var,
            'model_fields_var': model_fields_var,
            'view_model_class': view_model_class,
            'list_view_model_class': list_view_model_class,
            'url': url,
            'knockout_options': knockout_options,
            'ajax_options': ajax_options,
            'jquery': not settings.SETTINGS['disable_jquery'],
        }
    )

    return view_model_string


def ko_list_view_model(
    model_class,
    context=None,
    url=None,
    disable_ajax_options=False,
    include_list_utils=True,
):
    if not inspect.isclass(model_class):
        raise Exception('ko_view_model function requires a class')

    model_name = model_class.__name__
    model_list = model_name.lower() + 's'
    list_view_model_class = model_name + "ListViewModel"

    list_utils_string = (
        ko_list_utils(model_class) if include_list_utils else ''
    )

    view_model_string = ko_view_model(
        model_class,
        context=context,
        url=url,
        disable_ajax_options=disable_ajax_options,
    )

    list_view_model_string = render_to_string(
        "knockout/list_view_model.js",
        {
            'model_list': model_list,
            'list_view_model_class': list_view_model_class,
            'list_utils_string': list_utils_string,
            'view_model_string': view_model_string,
        }
    )

    return list_view_model_string


def ko_bindings(
    model_class,
    element_id=None,
    context=None,
    url=None,
    disable_ajax_data=False,
    disable_ajax_options=False,
    is_list=True,
):
    if not inspect.isclass(model_class):
        raise Exception('ko_bindings function requires a class')

    model_name = model_class.__name__
    l_model_name = model_name.lower()
    model_list = l_model_name + "s"
    model_options_var = l_model_name + '_options'
    model_data_var = l_model_name + '_data'
    view_model_class = model_name + "ViewModel"
    list_view_model_class = model_name + "ListViewModel"
    model_type = list_view_model_class if is_list else view_model_class
    bind_function = 'ko_bind'
    if element_id:
        bind_function += '_' + element_id

    if element_id is not None and '-' in element_id:
        raise Exception(
            'element_id cannot contain dashes: it is both an '
            'element id and a javascript variable'
        )

    if not url:
        url = _get_url(context, model_name)

    knockout_options = utils.get_knockout_options(model_class, None)

    if not disable_ajax_data:
        ajax_data = not settings.SETTINGS['disable_ajax_data']
    else:
        ajax_data = not disable_ajax_data

    if not disable_ajax_options:
        ajax_options = not settings.SETTINGS['disable_ajax_options']
    else:
        ajax_options = not disable_ajax_options

    bindings_string = render_to_string(
        "knockout/bindings.js",
        {
            'model_list': model_list,
            'model_options_var': model_options_var,
            'model_data_var': model_data_var,
            'view_model_class': view_model_class,
            'list_view_model_class': list_view_model_class,
            'element_id': element_id,
            'model_type': model_type,
            'bind_function': bind_function,
            'url': url,
            'knockout_options': knockout_options,
            'is_list': is_list,
            'ajax_data': ajax_data,
            'ajax_options': ajax_options,
            'jquery': not settings.SETTINGS['disable_jquery'],
        }
    )

    return bindings_string


def ko(
    model_class,
    element_id=None,
    context=None,
    url=None,
    disable_ajax_data=False,
    disable_ajax_options=False,
    is_list=True,
):
    if not inspect.isclass(model_class):
        raise Exception('ko function requires a class')

    model_string = None
    if disable_ajax_data and not is_list:
        view_model_string = ko_view_model(
            model_class,
            context=context,
            url=url,
            disable_ajax_options=disable_ajax_options,
        )

        model_string = view_model_string
    else:
        list_view_model_string = ko_list_view_model(
            model_class,
            context=context,
            url=url,
            disable_ajax_options=disable_ajax_options,
        )

        model_string = list_view_model_string

    bindings_string = ko_bindings(
        model_class,
        element_id=element_id,
        context=context,
        url=url,
        disable_ajax_data=disable_ajax_data,
        disable_ajax_options=disable_ajax_options,
        is_list=is_list,
    )

    ko_string = model_string + bindings_string

    return ko_string
