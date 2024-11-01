from django.urls import path
from .views import (DialogListCreateView,
    DialogDetailView,
    MessageListCreateView,
    MessageDetailView
)


urlpatterns = [

    path('dialogs/', DialogListCreateView.as_view(), name='dialog-list-create'),
    path('dialogs/<uuid:pk>/', DialogDetailView.as_view(), name='dialog-detail'),
    path('dialogs/<uuid:dialog_id>/messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<uuid:pk>/', MessageDetailView.as_view(), name='message-detail'),
    
]
