from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.conf import settings

class CustomUserManager(BaseUserManager):
    """Менеджер пользователя."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    """Модель пользователя."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    GENDER_TYPES = (
        ('девушка', "woman", ),
        ('парень', "man", ),
    )
    bio = models.TextField('Описание', max_length=500, blank=True)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField("Пол", choices=GENDER_TYPES, max_length=10, blank=True, default="не выбран")
    slug = models.SlugField(max_length=40, unique=True, blank=True)
    phone = models.CharField('Телефон', max_length=12, blank=True)
    email = models.EmailField('Email адрес', unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, null=True, blank=True)
    activation_code_created_at = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Генерация slug на основе username
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)  
        super().save(*args, **kwargs)
        
    @property
    def full_name(self):
        return '{} {}'.format(self.last_name, self.first_name)
        
    def __str__(self):
        return f'{self.username}: {self.first_name} - {self.email}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class PhotoGallery(models.Model):
    """Модель галереи фотографий пользователя."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField("Изображение", upload_to='photo_gallery/')
    created_at = models.DateTimeField("Дата добавления", auto_now_add=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return f'Фото {self.id} пользователя {self.user.email}'
    
    def get_image(self):
        if self.image:
            return f'{settings.BASE_URL}{self.image.url}'
        return ''
