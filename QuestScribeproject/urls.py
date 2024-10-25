from django.urls import include, path
from rest_framework import routers
from QuestScribeapi.views.journals import JournalEntryViewSet, TagViewSet
from QuestScribeapi.views.users import ProfileView, login_user, register_user,UserListView, UserProfileView
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
    path('api/profile/<int:pk>/', UserProfileView.as_view(), name='user-detail'),  # Fetch user by ID

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
