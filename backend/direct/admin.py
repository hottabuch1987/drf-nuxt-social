from django.contrib import admin
from .models import Dialog, Message

class MessageInline(admin.TabularInline):
    """Inline для отображения сообщений в диалоге."""
    model = Message
    extra = 1  # Количество пустых форм для добавления новых сообщений

@admin.register(Dialog)
class DialogAdmin(admin.ModelAdmin):
    """Админка для модели Dialog."""
    list_display = ('user1', 'user2', 'created_at')
    search_fields = ('user1__username', 'user2__username')
    list_filter = ('created_at',)
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Админка для модели Message."""
    list_display = ('sender', 'dialog', 'timestamp', 'status')
    search_fields = ('sender__username',)
    list_filter = ('status', 'timestamp')
    ordering = ('-timestamp',)
