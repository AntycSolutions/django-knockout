from django import forms
from django.forms import formsets, widgets

from knockout import utils


def render_data_bind_attr(
    field, field_name, click_checked=True, exclude=False
):
    attr = ""

    if exclude:
        return attr

    if field.value():
        attr += 'init, '

    widget = field.field.widget
    if isinstance(widget, widgets.CheckboxInput):
        if click_checked:
            attr += "click: clickChecked, "
        attr += "checked: {}".format(field_name)
    elif isinstance(widget, widgets.ClearableFileInput):
        attr += (
            "event: {{"
            "    change: function(data, event) {{"
            "        if (typeof {field_name}Change === 'function') {{"
            "            {field_name}Change(data, event);"
            "        }}"
            "    }}"
            "}}".format(field_name=field_name)
        )
    else:
        attr += "value: {}".format(field_name)

    return attr


class KnockoutModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(KnockoutModelForm, self).__init__(*args, **kwargs)

        # self (form) comes second, overrides model model
        knockout_options = utils.get_knockout_options(self._meta.model, self)

        for field in self:
            exclude, field_name = utils.get_knockout_field_options(
                field,
                knockout_options['knockout_fields'],
                knockout_options['knockout_exclude'],
                knockout_options['knockout_field_names'],
            )

            attr = render_data_bind_attr(
                field,
                field_name,
                click_checked=knockout_options['click_checked'],
                exclude=exclude,
            )

            if attr:
                field.field.widget.attrs['data-bind'] = attr


class KnockoutBaseInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(KnockoutBaseInlineFormSet, self).add_fields(form, index)

        attr = 'checked: DELETE'
        delete_field = form.fields[formsets.DELETION_FIELD_NAME]
        delete_field.widget.attrs['data-bind'] = attr
        delete_field.widget.attrs['class'] = 'formset-delete'
