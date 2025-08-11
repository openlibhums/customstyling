import os
import sys
import difflib

from django.conf import settings
from customstyling import plugin_settings

from utils.logger import get_logger
logger = get_logger(__name__)


def change_css_selectors(file_paths, changes_to_make, reverse=False):
    """
    Modifies custom stylesheets to update specific CSS selectors.
    Reverse allows this to be used for undo a migration as well.
    """
    for file_path in file_paths:
        try:
            css = []
            new_css = []
            with open(file_path, 'r', encoding="utf-8") as file_ref:
                css = file_ref.readlines()
                for line in css:
                    for theme, old, new in changes_to_make:
                        if theme.lower() in file_path.lower():
                            if reverse:
                                line = line.replace(new, old)
                            else:
                                line = line.replace(old, new)
                    new_css.append(line)
            if css != new_css:
                backup_file_folder = os.path.join(
                    os.path.dirname(file_path),
                    'temp',
                )
                if not os.path.exists(backup_file_folder):
                    os.mkdir(backup_file_folder)
                backup_file_path = os.path.join(
                    backup_file_folder,
                    os.path.basename(file_path),
                )
                with open(backup_file_path, 'w', encoding="utf-8") as file_ref:
                    file_ref.writelines(css)
                logger.info(f'Original backed up to {backup_file_path}')

                with open(file_path, 'w', encoding="utf-8") as file_ref:
                    file_ref.writelines(new_css)
                logger.info(f'Stylesheet modified at {file_path}')
                diff = difflib.unified_diff(css, new_css)
                sys.stdout.writelines(diff)
            else:
                pass
                # logger.info(f'No changes needed at {file_path}')

        except FileNotFoundError:
            pass
            # logger.info(f'No sheet found at {file_path}')


def get_custom_stylesheet_paths(apps, schema_editor):
    """
    Gets all custom stylesheet paths for journals and press.
    
    Returns:
        list: List of file paths to custom stylesheets
    """
    Journal = apps.get_model('journal', 'Journal')
    Press = apps.get_model('press', 'Press')
    SettingValue = apps.get_model('core', 'SettingValue')
    CrossJournalStylesheet = apps.get_model('customstyling', 'CrossJournalStylesheet')

    stylesheet_paths = []

    # Get journal stylesheets
    for journal in Journal.objects.all():
        journal_id = journal.id
        try:
            theme = SettingValue.objects.get(
                setting__group__name='general',
                setting__name='journal_theme',
                journal__id=journal_id,
            )
        except SettingValue.DoesNotExist:
            continue

        stylesheet_paths.extend([
            os.path.join(
                settings.BASE_DIR,
                'static',
                theme.value,
                'css',
                f'journal{journal_id}_override.css',
            ),
            os.path.join(
                plugin_settings.BASE_CSS_PATH,
                str(journal_id),
                'custom.css',
            )
        ])

        for sheet in CrossJournalStylesheet.objects.filter(journals=journal):
            stylesheet_paths.append(
                os.path.join(
                    plugin_settings.BASE_CSS_PATH,
                    'press',
                    sheet.stylesheet_name,
                )
            )

    # Get press stylesheets
    press = Press.objects.first()
    if press:
        stylesheet_paths.extend([
            os.path.join(
                settings.BASE_DIR,
                'static',
                press.theme,
                'css',
                'press_override.css',
            ),
            os.path.join(
                plugin_settings.BASE_CSS_PATH,
                'press',
                'custom.css',
            )
        ])

    return stylesheet_paths


def find_and_handle_custom_stylesheets(apps, schema_editor, changes_to_make, reverse=False):
    """
    Main function to find and process custom stylesheets with specified changes.
    
    Args:
        apps: Django apps registry
        schema_editor: Django schema editor
        changes_to_make: List of tuples with (theme, old_selector, new_selector)
        reverse: If True, reverses the changes
    """
    stylesheet_paths = get_custom_stylesheet_paths(apps, schema_editor)
    change_css_selectors(stylesheet_paths, changes_to_make, reverse=reverse) 