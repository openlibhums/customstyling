from utils import plugins

PLUGIN_NAME = 'Custom Styling Plugin'
DISPLAY_NAME = 'Custom Styling'
DESCRIPTION = 'Allows staff to add custom css to journals.'
AUTHOR = 'Andy Byers'
VERSION = '0.1'
SHORT_NAME = 'customstyling'
MANAGER_URL = 'customstyling_manager'
JANEWAY_VERSION = "1.3.8"


class CustomstylingPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION
    

def install():
    CustomstylingPlugin.install()


def hook_registry():
    return {
        'base_head_css':
            {
                'module': 'plugins.customstyling.hooks',
                'function': 'inject_css',
            },
    }


def register_for_events():
    pass
