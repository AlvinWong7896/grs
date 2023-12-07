from django.db import migrations, models


def set_default_main_photo(apps, schema_editor):
    Bike = apps.get_model("bikes", "Bike")
    # Set an empty string as the default value for main_photo
    Bike.objects.filter(main_photo__isnull=True).update(main_photo="")


class Migration(migrations.Migration):
    dependencies = [
        (
            "bikes",
            "0007_auto_20231206_1735",
        ),  # Adjust the dependency to the latest existing migration
    ]

    operations = [
        migrations.RunPython(set_default_main_photo),
    ]
