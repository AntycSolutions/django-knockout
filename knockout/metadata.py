import collections

# from django.utils.encoding import force_text

from rest_framework import metadata


class KnockoutMetadata(metadata.SimpleMetadata):
    """
    Return a more simplified version of SimpleMetaData
    """

    def determine_metadata(self, request, view):
        """
            Return the actions and raw meta data
        """
        metadata = collections.OrderedDict()

        # metadata['name'] = view.get_view_name()
        # metadata['description'] = view.get_view_description()
        # metadata['renders'] = [
        #     renderer.media_type for renderer in view.renderer_classes
        # ]
        # metadata['parses'] = [
        #     parser.media_type for parser in view.parser_classes
        # ]

        if hasattr(view, 'get_serializer'):
            actions = self.determine_actions(request, view)
            if actions:
                metadata.update(actions)

        return metadata

    def get_serializer_info(self, serializer):
        """
        Given an instance of a serializer, return a dictionary
        of it's fields and/or a list of it's child's fields.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child

        serializer_info = []
        for field_name, field in serializer.fields.items():
            field_info, has_child = self.get_field_info(field)
            if has_child:
                field_info = [field_info]

            serializer_info.append((field_name, field_info))

        return collections.OrderedDict(serializer_info)

    def get_field_info(self, field):
        """
        Return only fields and child's fields
        """
        field_info = collections.OrderedDict()
        # field_info['type'] = self.label_lookup[field]
        # field_info['required'] = getattr(field, 'required', False)

        # attrs = [
        #     'read_only', 'label', 'help_text',
        #     'min_length', 'max_length',
        #     'min_value', 'max_value'
        # ]
        # for attr in attrs:
        #     value = getattr(field, attr, None)
        #     if value is not None and value != '':
        #         field_info[attr] = force_text(value, strings_only=True)

        has_child = False
        if getattr(field, 'child', None):
            has_child = True

            child_field_info, child_has_child = self.get_field_info(
                field.child
            )
            if child_has_child:
                child_field_info = [child_field_info]

            field_info.update(child_field_info)
        elif getattr(field, 'fields', None):
            field_info.update(self.get_serializer_info(field))

        # if not field_info.get('read_only') and hasattr(field, 'choices'):
        #     field_info['choices'] = [
        #         {
        #             'value': choice_value,
        #             'display_name': force_text(
        #                 choice_name, strings_only=True
        #             )
        #         }
        #         for choice_value, choice_name in field.choices.items()
        #     ]

        if not field_info:
            # ko.mapping does not turn a dict nor OrderedDict into observables
            #  but will turn null into an observable. Django rest framework
            #  turns None into null
            field_info = None

        return field_info, has_child
