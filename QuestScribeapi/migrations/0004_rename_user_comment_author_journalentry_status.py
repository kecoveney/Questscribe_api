# Generated by Django 5.1.2 on 2024-10-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestScribeapi', '0003_tag_journalentry_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='author',
        ),
        migrations.AddField(
            model_name='journalentry',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=10),
        ),
    ]