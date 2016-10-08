from django.conf import settings

SETTINGS = {
    'disable_jquery': False,
    'disable_ajax_data': False,
    'disable_ajax_options': False,
}
SETTINGS.update(getattr(settings, 'DJANGO_KNOCKOUT', {}))
