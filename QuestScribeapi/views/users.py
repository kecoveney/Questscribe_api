from rest_framework import serializers, generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from QuestScribeapi.models import Profile, Notification
import json

# User and Profile Serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        Token.objects.create(user=user)  # Automatically create a token
        return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'display_name', 'bio', 'profile_photo', 'role', 'user_id', 'date_joined']


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'profile_photo', 'role']  # Allow updating of role


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile  # Access the Profile through the user
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile = request.user.profile  # Access the Profile through the user
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            req_body = json.loads(body)

            name = req_body['username']
            pass_word = req_body['password']
            authenticated_user = authenticate(username=name, password=pass_word)

            if authenticated_user is not None:
                token, created = Token.objects.get_or_create(user=authenticated_user)
                return JsonResponse({"valid": True, "token": token.key, "id": authenticated_user.id}, status=200)
            else:
                return JsonResponse({"valid": False, "error": "Invalid credentials"}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({"valid": False, "error": "Invalid JSON format"}, status=400)

    return HttpResponseNotAllowed(['POST'])


@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            req_body = json.loads(request.body.decode())

            required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
            if not all(field in req_body for field in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            new_user = User.objects.create_user(
                username=req_body['username'],
                email=req_body['email'],
                password=req_body['password'],
                first_name=req_body['first_name'],
                last_name=req_body['last_name']
            )

            token = Token.objects.create(user=new_user)
            data = json.dumps({"token": token.key, "id": new_user.id})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_201_CREATED)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

    return HttpResponseNotAllowed(['POST'])


class UserProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        user_id = self.kwargs['pk']  # Use 'pk' if your URL captures the ID as pk
        return Profile.objects.get(user_id=user_id)


# Following and Unfollowing Users
class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            followed_user = User.objects.get(pk=user_id)
            if request.user.profile.following.filter(pk=followed_user.id).exists():
                return Response({"error": "You are already following this user."}, status=400)
            
            # Follow the user
            request.user.profile.following.add(followed_user.profile)

            # Create a notification for the followed user
            Notification.objects.create(
                user=followed_user,
                notification_type='follow'
            )

            return Response({"success": f"You are now following {followed_user.username}"}, status=201)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

    def delete(self, request, user_id):
        try:
            followed_user = User.objects.get(pk=user_id)
            request.user.profile.following.remove(followed_user.profile)
            return Response({"success": f"You have unfollowed {followed_user.username}"}, status=204)

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)


class NotificationSerializer(serializers.ModelSerializer):
    journal_entry_title = serializers.CharField(source='journal_entry.title', read_only=True)
    comment_content = serializers.CharField(source='comment.content', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'journal_entry', 'journal_entry_title', 'comment', 'comment_content', 'created_at', 'is_read']



class NotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user).order_by('-created_at')
    
class NotificationDetailView(generics.DestroyAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        notification_id = self.kwargs['pk']
        return super().get_object()