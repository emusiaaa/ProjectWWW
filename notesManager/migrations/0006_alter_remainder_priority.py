# Generated by Django 4.1.4 on 2023-01-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notesManager', '0005_alter_remainder_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remainder',
            name='priority',
            field=models.IntegerField(choices=[(3, 'High'), (2, 'Medium'), (1, 'Low')]),
        ),
    ]
