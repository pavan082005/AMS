# Generated by Django 5.1.2 on 2024-11-02 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unitrader', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone_number',
            new_name='ph_number',
        ),
        migrations.AlterField(
            model_name='profile',
            name='roll_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]