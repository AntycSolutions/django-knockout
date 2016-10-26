from django.forms import forms, models  # type: ignore

import typing


def render_data_bind_attr(
    field: forms.BoundField,
    field_name: str,
    click_checked: bool=True,
    exclude: bool=False,
) -> str:
    ...


class KnockoutModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        ...


class KnockoutBaseInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(
        self, form: models.ModelFormMetaclass, index: typing.Optional[int]
    ) -> None:
        ...
