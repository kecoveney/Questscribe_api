from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Comment Model
class Comment(models.Model):
    journal_entry = models.ForeignKey('JournalEntry', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.journal_entry.title}'

from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('friends', 'Friends'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.ManyToManyField(User, related_name='liked_entries', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New fields
    character_name = models.CharField(max_length=100, blank=True, null=True)  # For character associated with the entry
    campaign_title = models.CharField(max_length=200, blank=True, null=True)  # For campaign or story arc
    session_number = models.PositiveIntegerField(blank=True, null=True)  # To track which session this belongs to
    location = models.CharField(max_length=200, blank=True, null=True)  # In-game location
    mood = models.CharField(max_length=50, blank=True, null=True)  # Emotional tone of the entry
    inspiration_points = models.PositiveIntegerField(default=0)  # Track inspiration points or bonuses
    word_count = models.PositiveIntegerField(default=0, blank=True)  # Automatically store word count
    privacy_level = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')  # Control entry visibility
    related_quest = models.CharField(max_length=200, blank=True, null=True)  # Related quest or mission

    # Tags (many-to-many relationship)
    tags = models.ManyToManyField('Tag', related_name='journal_entries', blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Automatically calculate word count before saving
        self.word_count = len(self.content.split())
        super().save(*args, **kwargs)

# Profile Model
class Profile(models.Model):
    USER_ROLES = [
        ('reader', 'Reader'),
        ('adventurer', 'Adventurer')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField()
    profile_photo = models.FileField(upload_to='profile_photos/', blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='reader')  # Add a role field with choices

    def __str__(self):
        return self.user.username
