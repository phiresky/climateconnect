# Generated by Django 2.2.13 on 2020-07-24 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('climateconnect_api', '0024_auto_20200723_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.CharField(blank=True, help_text='Website', max_length=256, null=True, verbose_name='City'),
        ),
    ]