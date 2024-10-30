from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.user_service import UserService, UserSerializer


class CustomUserCreate(APIView):
    '''Create a new user'''
    def post(self, request, format='json'):
        user_data = request.data
        result, success = UserService.create_user(user_data)
        if success:
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class  UserListView(APIView):
    '''List all users'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
