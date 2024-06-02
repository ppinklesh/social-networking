from django.urls import path
from .views import UserSignupView, UserLoginView, UserSearchView, SendFriendRequestView, ManageFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:id>/', ManageFriendRequestView.as_view(), name='manage-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]