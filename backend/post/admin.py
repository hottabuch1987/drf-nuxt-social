from django.contrib import admin

# Register your models here.
from .models import Category, Product, FavoriteProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category','slug',  'is_published']
    list_filter = [ 'name', 'date_added','slug', 'is_published']
    list_editable = ['is_published']
    prepopulated_fields = {'slug':('name',)}
    date_hierarchy ='date_added'


@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date_added')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user',)  # фильтруем по пользователю

