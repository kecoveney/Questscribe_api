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
from QuestScribeapi.models import Profile
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
    date_joined = serializers.DateTimeField(source='user.date_joined', read_only=True)  # Add this line

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'display_name', 'bio', 'profile_photo', 'role','user_id', 'date_joined']  # Include role


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'profile_photo', 'role']  # Allow updating of role

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Views

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

# Login and Registration Views

@csrf_exempt
def login_user(request):
    '''Handles the authentication of a user'''
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            req_body = json.loads(body)

            # Log username and password for debugging
            print(f"Username: {req_body.get('username')}, Password: {req_body.get('password')}")

            # Authenticate user
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
    '''Handles user registration'''
    if request.method == 'POST':
        try:
            req_body = json.loads(request.body.decode())

            # Validate required fields
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
            if not all(field in req_body for field in required_fields):
                return JsonResponse({"error": "Missing required fields"}, status=400)

            # Create new user
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

from rest_framework import generics

class UserProfileView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        # Get the user ID from the URL
        user_id = self.kwargs['pk']  # Use 'pk' if your URL captures the ID as pk
        # Return the Profile object related to that user
        return Profile.objects.get(user_id=user_id)
