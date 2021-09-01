from plugins.customstyling import models


def inject_css(context):
    request = context['request']
    if request.journal:
        styling = models.CustomStyling.objects.filter(
            journal=request.journal,
        ).first()

        if styling:
            print('hello')
            return '<link href="{}" rel="stylesheet">'.format(styling.url())

    return ''
