from django import forms
from django.forms import formsets, widgets


def render_data_bind_attr(field, field_name, click_checked=True):
    widget = field.field.widget
    if isinstance(widget, widgets.CheckboxInput):
        attr = ""
        if click_checked:
            attr += "click: clickChecked, "
        attr += "checked: {}".format(field_name)
    elif isinstance(widget, widgets.ClearableFileInput):
        attr = (
            "event: {{"
                " change: function(data, event) {{"
                    " if (typeof {field_name}Change === 'function') {{"
                        " {field_name}Change(data, event);"
                    " }}"
                " }}"
            " }}".format(field_name=field_name)
        )
    else:
        attr = "value: {}".format(field_name)

    return attr


class KnockoutModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(KnockoutModelForm, self).__init__(*args, **kwargs)

        if hasattr(self, 'knockout_field_names'):
            knockout_field_names = self.knockout_field_names
        else:
            knockout_field_names = {}

        if hasattr(self, 'knockout_exclude'):
            knockout_exclude = self.knockout_exclude
        else:
            knockout_exclude = []

        if hasattr(self, 'click_checked'):
            click_checked = self.click_checked
        else:
            click_checked = True

        for field in self:
            if field.name in knockout_exclude:
                continue

            if field.name in knockout_field_names:
                field_name = knockout_field_names[field.name]
            else:
                field_name = field.name

            attr = render_data_bind_attr(
                field, field_name, click_checked=click_checked
            )

            field.field.widget.attrs['data-bind'] = attr


class KnockoutBaseInlineFormSet(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(KnockoutBaseInlineFormSet, self).add_fields(form, index)

        attr = 'checked: DELETE'
        delete_field = form.fields[formsets.DELETION_FIELD_NAME]
        delete_field.widget.attrs['data-bind'] = attr
        delete_field.widget.attrs['class'] = 'formset-delete'
