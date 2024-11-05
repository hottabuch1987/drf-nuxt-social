from django.contrib import admin
from .models import User, PhotoGallery


class PhotoGalleryAdmin(admin.TabularInline):
    model = PhotoGallery
    extra = 1  # Количество пустых полей для добавления


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name',  'email', 'is_active']
    list_filter = [ 'first_name', 'last_name','slug', 'is_active']
    prepopulated_fields = {'slug':('username',)}
    date_hierarchy ='date_joined'
    search_fields = ('username', 'first_name', 'last_name', 'email')

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []  # Для администратора все поля будут редактируемыми
        else:
            return ('username', 'first_name', 'last_name', 'slug', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)  # Для персонала только указанные поля будут только для чтения

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    
    inlines = [PhotoGalleryAdmin]


admin.site.register(PhotoGallery)