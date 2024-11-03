from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import User, PhotoGallery


class PhotoGallerySerializer(serializers.ModelSerializer):
    '''Serializer photo gallery'''

    class Meta:
        model = PhotoGallery
        fields = ('id', 'image', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    '''Serializer user'''

    password = serializers.CharField(write_only=True)
    photos = PhotoGallerySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'first_name', 
            'last_name',
            'email', 
            'bio', 
            'birth_date', 
            'date_joined', 
            'is_active',
            'slug',
            'gender', 
            'phone',
            'password',
            'photos',
            'activation_code',
            'activation_code_created_at',

        )

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username', None),
        )
        return user
    
    
    
class EditUserSerializer(serializers.ModelSerializer):
    '''Serializer edit user'''

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'first_name', 
            'last_name',
            'email', 
            'bio', 
            'birth_date', 
            'date_joined', 
            'gender',
            'phone',
    
        )
    def validate(self, data):
        birth_date = data.get('birth_date')

        if birth_date is not None:  # Проверяем, что birth_date предоставлена
            # Вычисляем возраст
            today = datetime.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            # Валидация возраста
            if age < 16 or age > 99:
                raise ValidationError("Возраст должен быть между 16 и 99.")
        return data

    
class ChangePasswordSerializer(serializers.Serializer):
    '''Change password'''
    password = serializers.CharField(required=True)



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'is_active', 
            'gender', 
            'phone', 
            'slug', 
            'date_joined', 
            'birth_date'
            )