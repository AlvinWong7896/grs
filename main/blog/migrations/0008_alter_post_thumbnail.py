# Generated by Django 4.2.10 on 2024-05-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=models.ImageField(default='images/default_photo.jpg', upload_to='images/'),
        ),
    ]
