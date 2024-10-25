# Generated by Django 5.1.2 on 2024-10-17 16:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestScribeapi', '0004_rename_user_comment_author_journalentry_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalentry',
            name='adventurer',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='following',
        ),
        migrations.RemoveField(
            model_name='reader',
            name='user',
        ),
        migrations.RemoveField(
            model_name='journalentry',
            name='status',
        ),
        migrations.AddField(
            model_name='journalentry',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Adventurer',
        ),
        migrations.DeleteModel(
            name='Reader',
        ),
    ]
