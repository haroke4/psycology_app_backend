# Generated by Django 4.2.2 on 2023-06-21 17:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_audiometa_count_of_audios'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiometa',
            name='changed_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
