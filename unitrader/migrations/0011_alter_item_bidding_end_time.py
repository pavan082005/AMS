# Generated by Django 5.1.2 on 2024-11-04 07:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitrader', '0010_alter_item_bidding_end_time_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='bidding_end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
