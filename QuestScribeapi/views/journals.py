from rest_framework import serializers, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.models import JournalEntry, Comment, Tag
from django.db.models import Q

# Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_username', 'content', 'created_at']


# Tag Serializer
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

    def create(self, validated_data):
        name = validated_data.get('name', None).lower()
        tag, created = Tag.objects.get_or_create(name=name)
        return tag


# Journal Entry Serializer
class JournalEntrySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = JournalEntry
        fields = [
            'id', 'user_id', 'title', 'content', 'tags', 'status', 'likes_count', 
            'created_at', 'updated_at', 'character_name', 'campaign_title', 
            'session_number', 'location', 'mood', 'privacy_level', 
            'related_quest', 'word_count', 'comments'
        ]


# Journal Entry ViewSet
class JournalEntryViewSet(viewsets.ModelViewSet):
    queryset = JournalEntry.objects.all()
    serializer_class = JournalEntrySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'character_name', 'campaign_title']  # Fields to search
    ordering_fields = ['created_at', 'title']  # Fields to order by

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # Filter to show only public journals or the user's own private journals
        queryset = queryset.filter(
            Q(privacy_level="public") | Q(user=user)
        )

        # Additional filtering by user if 'user_only=true' is passed
        user_only = self.request.query_params.get('user_only', None)
        if user_only and user_only.lower() == 'true':
            queryset = queryset.filter(user=user)

        return queryset

    def perform_create(self, serializer):
        # Automatically save journal entry with the logged-in user
        journal_entry = serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        journal_entry = self.get_object()
        user = request.user

        # Check if the user already liked the journal
        if journal_entry.likes.filter(id=user.id).exists():
            # If already liked, remove the like (unlike)
            journal_entry.likes.remove(user)
        else:
            # Otherwise, add the like
            journal_entry.likes.add(user)

        return Response({'status': 'like toggled'})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_comment(self, request, pk=None):
        journal_entry = self.get_object()
        comment_content = request.data.get('content')
        if not comment_content:
            return Response({'error': 'Comment content required'}, status=400)

        comment = Comment.objects.create(
            journal_entry=journal_entry,
            author=request.user,
            content=comment_content
        )
        return Response(CommentSerializer(comment).data, status=201)


# Tag ViewSet
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
