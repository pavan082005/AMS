# Generated by Django 5.1.2 on 2024-11-04 06:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitrader', '0008_profile_coins'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='bidding_end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
