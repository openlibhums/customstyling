from django.db import migrations
from customstyling.utils import find_and_handle_custom_stylesheets


def forward_migration(apps, schema_editor):
    changes_to_make = [
        ('olh', '#content aside h2', '#content aside h3'),
        ('olh', '#content aside', '#content .side-info'),
    ]
    find_and_handle_custom_stylesheets(apps, schema_editor, changes_to_make, reverse=False)


def reverse_migration(apps, schema_editor):
    changes_to_make = [
        ('olh', '#content .side-info h2', '#content .side-info h3'),
        ('olh', '#content aside', '#content .side-info'),
    ]
    find_and_handle_custom_stylesheets(apps, schema_editor, changes_to_make, reverse=True)


class Migration(migrations.Migration):

    dependencies = [
        ('customstyling', '0002_upgrade_materialize'),
    ]

    operations = [
        migrations.RunPython(
            forward_migration,
            reverse_code=reverse_migration,
        )
    ] 