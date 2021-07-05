# Generated by Django 2.2.20 on 2021-06-24 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0015_ideatranslation_is_manual_translation'),
        ('climateconnect_api', '0060_auto_20210420_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='idea_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification_idea_comment', to='ideas.IdeaComment', verbose_name='Idea Comment'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.IntegerField(choices=[(0, 'broadcast'), (1, 'private_message'), (2, 'project_comment'), (3, 'reply_to_project_comment'), (4, 'project_follower'), (5, 'project_update_post'), (6, 'post_comment'), (7, 'reply_to_post_comment'), (8, 'group_message'), (11, 'idea_comment'), (12, 'reply_to_idea_comment')], default=0, help_text='type of notification', verbose_name='Notification type'),
        ),
    ]
