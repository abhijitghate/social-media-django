from django.urls import path

from . import views

urlpatterns = [
    path("", views.FriendRequestView.as_view()),
    path("<int:pk>/", views.FriendRequestView.as_view()),
    path("update/<int:pk>/", views.FriendRequestUpdateStatusView.as_view()),
    path("create/", views.FriendRequestCreateView.as_view()),
    path("myfriends/", views.MyFriendsView.as_view()),
    path("pending/", views.PendingFriendRequests.as_view()),
]
