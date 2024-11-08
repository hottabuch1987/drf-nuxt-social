from django.urls import path
from .views import (
    LatesProductsList,
    search,
    ProductDetail,
    CategoryList,
    CategoryUserView,
    DetailCategoryUserView,
    ProductUserView,
    DetailProductUserView,
    FavoriteProductView
)


urlpatterns = [
    path('trenings/', LatesProductsList.as_view(), name='latest-products'),
    path('trening/search/', search, name='search-products'),
    path('trening/<slug:product_slug>/', ProductDetail.as_view(), name='product-detail'),
    path('trening-category/', CategoryList.as_view(), name='category-list'),
    path('my-category/', CategoryUserView.as_view(), name='my-categories'),
    path('my-category/<slug:slug>/', DetailCategoryUserView.as_view(), name='detail-category'),
    path('my-products/', ProductUserView.as_view(), name='my-products'),
    path('my-product/<slug:slug>/', DetailProductUserView.as_view(), name='detail-product'),
    path('favorites/', FavoriteProductView.as_view(), name='favorites')
   
]

