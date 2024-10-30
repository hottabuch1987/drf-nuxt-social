from django.urls import path, include
from .views import UserListView, CustomUserCreate
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView



urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path('users/', UserListView.as_view(), name='users'),  
   
]