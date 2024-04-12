from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.pagination import PageNumberPagination
from .models import User
from .serializers import CustomUserSerializer, UserRegisterSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q


class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    search_fields = ["username", "email", "first_name", "last_name"]

    def get(self, request):
        paginator = PageNumberPagination()
        queryset = User.objects.all()
        search_term = request.query_params.get("search")
        if search_term:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": search_term})
            queryset = queryset.filter(query)

        result_page = paginator.paginate_queryset(queryset, request)
        serializer = CustomUserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(
    [
        "POST",
    ]
)
def logout_user(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"Message": "You are logged out"}, status=status.HTTP_200_OK)


@api_view(
    [
        "POST",
    ]
)
def user_register_view(request):
    if request.method == "POST":
        serializer = UserRegisterSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.save()

            data["response"] = "Account has been created"
            data["username"] = user.email
            data["email"] = user.email

            refresh = RefreshToken.for_user(user)
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        else:
            data = serializer.errors
        return Response(data)
