from django.urls import path, include
from .views  import LatesProductsList, search, ProductDetail, CategoryList, CategoryUserView, DetailCategoryUserView, ProductUserView, DetailProductUserView


urlpatterns = [
    path('trenings/', LatesProductsList.as_view()),
    path('trening/search/', search),
    path('trening/<slug:product_slug>/', ProductDetail.as_view()),
    path('trening-category/', CategoryList.as_view()),
    path('my-category/', CategoryUserView.as_view(), name='programm'),
    path('my-category/<slug:slug>/', DetailCategoryUserView.as_view(), name='create-update-delete-program'),
    path('my-products/', ProductUserView.as_view(), name='program'),
    path('my-product/<slug:slug>/', DetailProductUserView.as_view(), name='create-update-delete-program'),




] 