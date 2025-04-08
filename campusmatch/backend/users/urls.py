from django.urls import path
from .views import (
    RegisterUserView, LoginUserView, UpdateProfileView, MatchUsersView,
    SendMessageView, NotificationView, SwipeUserView, register, chat,
    profile_settings, notifications,  index
)

urlpatterns = [
    path("", index, name="home"),
    path("login/", login),
    path("chat/<int:match_id>/", chat, name="chat"),
    path("profile/", profile_settings, name="profile_settings"),
    path("notifications/", notifications, name="notifications"),

    # API Endpoints
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/login/', LoginUserView.as_view(), name='login'),
    path('api/update-profile/', UpdateProfileView.as_view(), name='update-profile'),
    path('api/match/', MatchUsersView.as_view(), name='match'),
    path('api/send-message/', SendMessageView.as_view(), name='send-message'),
    path('api/notifications/<str:uid>/', NotificationView.as_view(), name='notifications'),
    path('api/swipe/', SwipeUserView.as_view(), name='swipe'),
]
