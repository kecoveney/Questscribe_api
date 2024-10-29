from django.urls import include, path
from rest_framework import routers
from QuestScribeapi.views.journals import JournalEntryViewSet, TagViewSet
from QuestScribeapi.views.users import ProfileView, login_user, register_user,NotificationListView,UserListView, UserProfileView, FollowView, NotificationDetailView
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'journals', JournalEntryViewSet)
router.register(r'tags', TagViewSet)  # Registering TagViewSet with the router

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register', register_user),
    path('api/login', login_user),
    path('api/profile', ProfileView.as_view()),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/profile/<int:pk>/', UserProfileView.as_view(), name='user-detail'), 
    path('follow/<int:user_id>/', FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', FollowView.as_view(), name='unfollow_user'), # Fetch user by ID
    path('api/notifications/', NotificationListView.as_view(), name='notification-list'),
    path('api/notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
