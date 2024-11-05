from django.urls import path, include
from .views import UserListView, CustomUserCreate, MeView, ProfileEditView, ChangePasswordView, DeleteUserView, UserDetail, VerifyUser, ResendActivationCode, PhotoGalleryView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('verify/', VerifyUser.as_view(), name='verify_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('resend-code/', ResendActivationCode.as_view(), name='resend-code'),
    path('account/', MeView.as_view(), name='account'),
    path('edit-account/', ProfileEditView.as_view(), name='edit-account'),
    path('user-foto/', PhotoGalleryView.as_view(), name='edit-foto'),
    path('user-foto/<int:pk>/', PhotoGalleryView.as_view(), name='photo_gallery_detail'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'), 
    path('users/', UserListView.as_view(), name='users'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('delete-user/', DeleteUserView.as_view(), name='delete_user'),
    path('user/<slug:slug>/', UserDetail.as_view(), name='user-detail'),
]
