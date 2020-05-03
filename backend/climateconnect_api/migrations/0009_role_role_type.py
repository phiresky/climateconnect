# Generated by Django 2.2.11 on 2020-05-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climateconnect_api', '0008_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='role_type',
            field=models.IntegerField(choices=[(0, 'read only'), (1, 'read write'), (2, 'all')], default=0, help_text='Type of role', verbose_name='Role Type'),
        ),
    ]
