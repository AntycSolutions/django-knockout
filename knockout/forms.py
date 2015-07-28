from django import forms


class KnockoutForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self:
            attr = "init, "

            if field.field.widget.__class__.__name__ in ['CheckboxInput']:
                attr += "click: $root.clickChecked, checked: "
            else:
                attr += "value: "

            attr += field.name

            field.field.widget.attrs['data-bind'] = attr
