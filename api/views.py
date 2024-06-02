from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer
from .models import FriendRequest
from .serializers import FriendRequestSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view


def rate_limit_exceeded(request, exception):
    return JsonResponse({'detail': 'Rate limit exceeded'}, status=429)

class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserSearchPagination(PageNumberPagination):
    page_size = 10

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if '@' in query:
            # Search by email
            return User.objects.filter(email__iexact=query)
        else:
            # Search by name
            return User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))



class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {'from_user': request.user.id, 'to_user': request.data['to_user']}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @ratelimit(key='user', rate='3/m', method='POST', block=True)
    @api_view(['POST'])
    def send_friend_request(request):
        return SendFriendRequestView.as_view()(request)

class ManageFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        action = request.data.get('action')
        if action == 'accept':
            request.user.friends.add(friend_request.from_user)
            friend_request.from_user.friends.add(request.user)
        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user)




