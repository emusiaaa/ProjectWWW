# Generated by Django 4.1.4 on 2023-01-22 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesManager', '0003_remainder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remainder',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
