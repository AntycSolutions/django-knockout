from django import forms


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

        if hasattr(self, 'knockout_init'):
            knockout_init = self.knockout_init
        else:
            knockout_init = False

        for field in self:
            if field.name in knockout_exclude:
                continue

            attr = ""

            if knockout_init:
                attr = "init, "

            widget_name = field.field.widget.__class__.__name__
            if widget_name in ['CheckboxInput']:
                attr += "click: $root.clickChecked, checked: "
            elif widget_name in ['ClearableFileInput']:
                pass
            else:
                attr += "value: "

            if field.name in knockout_field_names:
                attr += knockout_field_names[field.name]
            else:
                attr += field.name

            field.field.widget.attrs['data-bind'] = attr
