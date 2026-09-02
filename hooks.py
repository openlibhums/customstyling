import os

from plugins.customstyling import plugin_settings, models
from utils.function_cache import cache


def stylesheet_link(*path_parts):
    """
    Builds a link tag for a custom stylesheet, versioned with the file's
    mtime so browsers refetch it after an edit.
    """
    href = os.path.join(plugin_settings.CSS_MEDIA_PATH, *path_parts)
    file_path = os.path.join(plugin_settings.BASE_CSS_PATH, *path_parts)

    try:
        href = '{href}?v={version}'.format(
            href=href,
            version=int(os.path.getmtime(file_path)),
        )
    except OSError:
        # No file on disk yet; emit the link unversioned.
        pass

    return '<link href="{}" rel="stylesheet">\n'.format(href)


@cache(900)
def inject_css(context):
    request = context['request']
    html = ''
    if request.journal:
        cross_journal_stylesheets = models.CrossJournalStylesheet.objects.filter(
            journals=request.journal,
        )
        for stylesheet in cross_journal_stylesheets:
            html += stylesheet_link('press', stylesheet.stylesheet_name)
        html += stylesheet_link(str(request.journal.pk), 'custom.css')
    elif request.repository:
        html += stylesheet_link(
            'repositories',
            str(request.repository.pk),
            'custom.css',
        )
    else:
        html += stylesheet_link('press', 'custom.css')

    return html
