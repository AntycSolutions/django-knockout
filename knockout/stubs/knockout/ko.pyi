from django.db.models import base  # type: ignore
from django.template import context  # type: ignore

import typing


MB = typing.TypeVar('MB', bound=base.ModelBase)


def ko_list_utils(model_class: typing.Type[MB]) -> str:
    ...


def _get_url(context: context.RequestContext, model_name: str) -> str:
    ...


def ko_view_model(
    model_class: typing.Type[MB],
    context: typing.Optional[context.RequestContext]=None,
    url: typing.Optional[str]=None,
    disable_ajax_options: typing.Optional[bool]=None,
) -> str:
    ...


def ko_list_view_model(
    model_class: typing.Type[MB],
    context: typing.Optional[context.RequestContext]=None,
    url: typing.Optional[str]=None,
    disable_ajax_options: typing.Optional[bool]=None,
    include_list_utils: typing.Optional[bool]=True,
) -> str:
    ...


def ko_bindings(
    model_class: typing.Type[MB],
    element_id: typing.Optional[str]=None,
    context: typing.Optional[context.RequestContext]=None,
    url: typing.Optional[str]=None,
    disable_ajax_data: typing.Optional[bool]=None,
    disable_ajax_options: typing.Optional[bool]=None,
    is_list: typing.Optional[bool]=True,
) -> str:
    ...


def ko(
    model_class: typing.Type[MB],
    element_id: typing.Optional[str]=None,
    context: typing.Optional[context.RequestContext]=None,
    url: typing.Optional[str]=None,
    disable_ajax_data: typing.Optional[bool]=None,
    disable_ajax_options: typing.Optional[bool]=None,
    is_list: typing.Optional[bool]=True,
) -> str:
    ...
