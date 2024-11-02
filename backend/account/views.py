import random
import string
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .services.user_service import UserService, UserSerializer
from .models import User
from .serializers import UserSerializer, EditUserSerializer, ChangePasswordSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_verification_email



class CustomUserCreate(APIView):
    '''Create a new user'''

        

    def generate_verification_code(self):
        """Генерация случайного кода для подтверждения."""

        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) 
    
    
    def post(self, request, format='json'):
        user_data = request.data
        # Создание пользователя

        result, success = UserService.create_user(user_data)
        if success:
            code = self.generate_verification_code()  # Генерация кода
            email = user_data.get('email')
            # Отправляем код на электронную почту
            send_verification_email.delay(email, code)  # Запускаем задачу Celery
   
            return Response(result, status=status.HTTP_201_CREATED)

        

        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        users = User.objects.order_by('-date_joined').filter(is_active=True)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class MeView(APIView):
    '''Get current user'''
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
class BlacklistTokenUpdateView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        serializer = EditUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data.get('password')
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug, format=None):
        user = get_object_or_404(User, slug=slug)
        serializer = UserSerializer(user)
        return Response(serializer.data)