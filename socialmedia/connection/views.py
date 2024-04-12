from traceback import print_tb
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from user.models import User
from rest_framework.throttling import UserRateThrottle


from .models import FriendRequest
from .serializers import FriendRequestSerializer



class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = FriendRequest.objects.all()
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = FriendRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    def delete(self, request, pk):
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend Request not found'}, status=status.HTTP_404_NOT_FOUND)

        friend_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MyFriendsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        if not request.user:
            return Response({"error":"No user provided"})
        paginator = PageNumberPagination()
        queryset = FriendRequest.objects.filter(
            sent_by__email=request.user,
            status='accepted'
        )
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = FriendRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class PendingFriendRequests(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request):
        queryset = FriendRequest.objects.filter(
            status='pending'
        )
        if request.user and request.user.is_staff == False:
            queryset = queryset.filter(sent_by__email=request.user)   
        
        paginator = PageNumberPagination()

        print(">>", request.user, request.user.is_staff)
        
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = FriendRequestSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FriendRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        user = User.objects.get(email=request.user)

        existing_friend_requests = FriendRequest.objects.filter(
            sent_by__email=request.user,
            sent_to=request.data['sent_to'],
            status__in=['pending', 'accepted']
        )
        if existing_friend_requests:
            return Response({"message":"You are already friends or there is a active friend request"})
        
        if user.id != request.data["sent_by"]:
            return Response({'error': "Can not send request on someone else's behalf"})
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class FriendRequestUpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        user = User.objects.get(email=request.user)
        new_status = request.data.get("status", None)
        try:
            friend_request = FriendRequest.objects.get(pk=pk)
            if new_status in ['accepted', 'rejected'] and user.id != friend_request.sent_to.id:
                return Response({"error":"Friend Request can be accepted or rejected by someone who it is sent to"})
            if new_status == 'canceled' and user.id != friend_request.sent_by.id:
                return Response({"error":"Friend Request can be canceled by someone who it is sent by"})
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend Request not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FriendRequestSerializer(friend_request, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)