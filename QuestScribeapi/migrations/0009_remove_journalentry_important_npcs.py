# Generated by Django 5.1.2 on 2024-10-21 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuestScribeapi', '0008_journalentry_campaign_title_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='journalentry',
            name='important_npcs',
        ),
    ]