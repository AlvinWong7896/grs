# Generated by Django 4.2.10 on 2024-03-18 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_item_type_alter_item_material'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
    ]
