# Generated by Django 2.2.19 on 2022-02-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20220130_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
