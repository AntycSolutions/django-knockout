from django.db import models  # type: ignore
from django.db.models import query, base  # type: ignore
from django.template import context  # type: ignore
from django.forms import forms  # type: ignore

import typing


M = typing.TypeVar('M', bound=models.Model)
MB = typing.TypeVar('MB', bound=base.ModelBase)


def _get_model_class(
    values: typing.Union[list, query.QuerySet, typing.Type[MB], typing.Type[M]]
) -> M:
    ...


def knockout(
    context: typing.Optional[context.RequestContext],
    values: typing.Union[
        list, query.QuerySet, typing.Type[MB], typing.Type[M]
    ],
    element_id: typing.Optional[str]=None,
    url: typing.Optional[str]=None,
    disable_ajax_data: typing.Optional[bool]=False,
    is_list: typing.Optional[bool]=True
) -> str:
    ...


def knockout_list_view_model(
    context: typing.Optional[context.RequestContext],
    values: typing.Union[
        list, query.QuerySet, typing.Type[MB], typing.Type[M]
    ],
    url: typing.Optional[str]=None
) -> str:
    ...


def knockout_bindings(
    context: typing.Optional[context.RequestContext],
    values: typing.Union[
        list, query.QuerySet, typing.Type[MB], typing.Type[M]
    ],
    element_id: typing.Optional[str]=None,
    url: typing.Optional[str]=None,
    disable_ajax_data: typing.Optional[bool]=False,
    is_list: typing.Optional[bool]=True
) -> str:
    ...


def knockout_view_model(
    context: typing.Optional[context.RequestContext],
    values: typing.Union[
        list, query.QuerySet, typing.Type[MB], typing.Type[M]
    ],
    url: typing.Optional[str]=None
) -> str:
    ...


def knockout_list(
    values: typing.Union[
        list, query.QuerySet, typing.Type[MB], typing.Type[M]
    ],
) -> str:
    ...


def data_bind(field: forms.BoundField) -> str:
    ...
