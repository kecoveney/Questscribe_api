# Generated by Django 5.1.2 on 2024-10-17 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestScribeapi', '0006_journalentry_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
