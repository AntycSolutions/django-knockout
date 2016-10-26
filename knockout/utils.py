
def get_knockout_options(model_class, form):
    knockout_options = {
        'knockout_exclude': [],
        'knockout_fields': [],
        'knockout_field_names': [],
        'click_checked': True,
    }

    for item in (model_class, form):
        if not item:
            continue

        has_fields_and_exclude = (
            hasattr(item, 'knockout_exclude') and
            hasattr(item, 'knockout_fields')
        )
        if has_fields_and_exclude:
            raise Exception(
                'Define knockout_exclude or knockout_fields, not both'
            )

        for option, default in knockout_options.items():
            if hasattr(item, option):
                value = getattr(item, option)
                if callable(value):
                    knockout_options[option] = value()
                else:
                    knockout_options[option] = value

    return knockout_options


def get_knockout_field_options(
    field,
    knockout_fields,
    knockout_exclude,
    knockout_field_names
):
    exclude = (
        (knockout_fields and field.name not in knockout_fields) or
        (field.name in knockout_exclude)
    )

    if field.name in knockout_field_names:
        field_name = knockout_field_names[field.name]
    else:
        field_name = field.name

    return exclude, field_name
