# Generated by Django 4.2.10 on 2024-02-21 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_rename_created_post_created_on"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="updated",
            new_name="updated_on",
        ),
    ]
