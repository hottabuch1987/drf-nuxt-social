from django.db import models
from account.models import User
from django.conf import settings
from slugify import slugify


class Category(models.Model):
    owner = models.ForeignKey(User, related_name='categories', on_delete=models.CASCADE, verbose_name='Владелец категории')
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(verbose_name='слаг')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    

    def save(self, *args, **kwargs):
        # Проверяем, изменилось ли имя категории
        if self.pk is None or self.name != Category.objects.get(pk=self.pk).name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Проверяем уникальность слага
            while Category.objects.filter(slug=slug, owner=self.owner).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'
    
  
    


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='категория')
    name = models.CharField(max_length=255, verbose_name='имя')
    slug = models.SlugField(verbose_name='слаг')
    description = models.TextField(blank=True, null=True, verbose_name='описание поста')
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name='фото')
    video = models.FileField(upload_to='videos/', blank=True, null=True, verbose_name='видео')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано') 

    
    def save(self, *args, **kwargs):
        # Проверяем, изменилось ли имя продукта
        if self.pk is None or (
            self.pk is not None and self.name != Product.objects.get(pk=self.pk).name
        ):
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Проверяем уникальность слага
            while Product.objects.filter(slug=slug, category=self.category).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)



    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-date_added',)

    def __str__(self):
        return  self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return f'{settings.BASE_URL}{self.image.url}'
        return ''

    def get_video(self):
        if self.video:
            return f'{settings.BASE_URL}{self.video.url}'
        return ''
    


