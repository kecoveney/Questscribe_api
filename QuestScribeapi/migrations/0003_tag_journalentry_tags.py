# Generated by Django 5.1.2 on 2024-10-17 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuestScribeapi', '0002_profile_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='journalentry',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='journal_entries', to='QuestScribeapi.tag'),
        ),
    ]
