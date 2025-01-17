# Generated by Django 2.2.24 on 2021-10-26 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0085_organization_hubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Time when the user liked the project', verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now_add=True, help_text='Time when the like was updated', verbose_name='Updated At')),
                ('project', models.ForeignKey(help_text='Points to a project', on_delete=django.db.models.deletion.CASCADE, related_name='project_liked', to='organization.Project', verbose_name='Project')),
                ('user', models.ForeignKey(help_text='Points to the user who liked the project', on_delete=django.db.models.deletion.CASCADE, related_name='liking_user', to=settings.AUTH_USER_MODEL, verbose_name='Liking User')),
            ],
            options={
                'verbose_name': 'Project Like',
                'verbose_name_plural': 'Project Likes',
                'ordering': ['-id'],
            },
        ),
    ]
