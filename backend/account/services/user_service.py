from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.serializers import UserSerializer


class UserService: 
    @staticmethod
    def create_user(data):      
        email = data.get('email')
        username = data.get('username')
        
        if User.objects.filter(email=email).exists():
            return {"error": "Пользователь с таким email уже существует."}, False
        
        if User.objects.filter(username=username).exists():
            return {"error": "Пользователь с таким именем уже существует."}, False
            
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return serializer.data, True
            
        return serializer.errors, False

    @staticmethod
    def generate_tokens(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
