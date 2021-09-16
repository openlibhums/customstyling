import os

from plugins.customstyling import plugin_settings


def inject_css(context):
    request = context['request']
    if request.journal:
        return '<link href="{}" rel="stylesheet">'.format(
            os.path.join(plugin_settings.CSS_MEDIA_PATH, str(request.journal.pk), 'custom.css')
        )

    return ''
