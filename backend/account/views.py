import random
import string
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, PhotoGallery
from .serializers import UserSerializer, ChangePasswordSerializer, EditUserSerializer, UserListSerializer, PhotoGallerySerializer
from .tasks import send_verification_email
from .services.user_service import UserService


class CustomUserCreate(APIView):
    '''Create a new user'''

    def generate_verification_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def post(self, request, format='json'):
        user_data = request.data
        result, success = UserService.create_user(user_data)

        if success:
            code = self.generate_verification_code()
            email = user_data.get('email')

            user = User.objects.get(email=email)
            user.activation_code = code
            user.activation_code_created_at = timezone.now()
            user.is_active = False
            user.save()

            request.session['activation_email'] = email
            print("Сохраненный email в сессии:", request.session.get('activation_email'))

            send_verification_email.delay(email, code)
            return Response(result, status=status.HTTP_201_CREATED)

        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    '''Verify user by activation code'''

    def post(self, request, format='json'):
        code = request.data.get('code')
        email = request.session.get('activation_email')

        if not code:
            return Response({"message": "Код активации не указан."}, status=status.HTTP_400_BAD_REQUEST)

        print("Полученный email из сессии:", email)
        if not email:
            return Response({"message": "Email не найден в сессии."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            # Проверка времени действия кода активации
            if user.activation_code_created_at:
                time_diff = timezone.now() - user.activation_code_created_at
                if time_diff.total_seconds() > 300:  # Код действителен 5 минут
                    return Response({"message": "Код активации устарел."}, status=status.HTTP_400_BAD_REQUEST)
            # Проверка кода активации
            if user.activation_code == code:
                user.is_active = True
                user.activation_code = None
                user.activation_code_created_at = None
                user.save()
                # Удаляем email из сессии после успешной активации
                request.session.pop('activation_email', None)
                return Response({"message": "Пользователь успешно активирован."}, status=status.HTTP_200_OK)
            return Response({"message": "Неверный код активации."}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)


class ResendActivationCode(APIView):
    '''Resend activation code'''

    def generate_verification_code(self):
        """Генерация случайного кода для подтверждения."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def post(self, request, format='json'):
        email = request.session.get('activation_email')

        if not email:
            return Response({"message": "Email не указан."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            code = self.generate_verification_code()  # Генерация нового кода
            user.activation_code = code
            user.activation_code_created_at = timezone.now()  # Обновляем время создания кода
            user.save()

            # Сохраняем email в сессии, если нужно
            request.session['activation_email'] = email

            send_verification_email.delay(email, code)  # Отправляем новый код
            return Response({"message": "Код активации повторно отправлен."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    '''Custom token obtain pair view'''

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        # проверяя, активен ли пользователь
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response({"detail": "Пользователь не активирован."}, status=status.HTTP_403_FORBIDDEN)

            if user.check_password(password):
                return super().post(request, *args, **kwargs)
            else:
                return Response({"detail": "Неверный пароль."}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден."}, status=status.HTTP_404_NOT_FOUND)



class MeView(APIView):
    '''Get current user'''

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
class BlacklistTokenUpdateView(APIView):
    '''Blacklist token'''

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserListView(APIView):
    '''List all users'''

    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        users = User.objects.filter(is_active=True).order_by('-date_joined')
        serializer = UserListSerializer(users, many=True)
        return Response(serializer.data)
    

class ProfileEditView(APIView):
    '''Edit profile'''

    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        user = request.user
        serializer = EditUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    '''Çhange password'''

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

class PhotoGalleryView(APIView):
    '''Get photo gallery'''

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем только фотографии текущего пользователя
        photos = PhotoGallery.objects.filter(user=request.user)
        serializer = PhotoGallerySerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        serializer = PhotoGallerySerializer(data=request.data)
        if serializer.is_valid():
            # Указываем пользователя при сохранении
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):         
        try:
            # Убедитесь, что удаляем только ту фотографию, которая принадлежит текущему пользователю
            photo = PhotoGallery.objects.get(pk=pk, user=request.user)
            photo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PhotoGallery.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DeleteUserView(APIView):
    '''Delete user'''

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UserDetail(APIView):
    '''Get user by slug'''
    
    permission_classes = [IsAuthenticated]
    def get(self, request, slug, format=None):
        user = get_object_or_404(User, slug=slug)
        serializer = UserSerializer(user)
        return Response(serializer.data)