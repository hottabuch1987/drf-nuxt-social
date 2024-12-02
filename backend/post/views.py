from django.db.models import Q
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import  status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer, FavoriteProductSerializer
from .models import Product, Category, FavoriteProduct
#from .tasks import send_order_email, delete_order


class LatesProductsList(APIView):
  def get(self, request, format=None):
        products = Product.objects.filter(is_published=True).order_by('-date_added', )
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
  

class ProductDetail(APIView):
    def get_object(self, product_slug):
        try:
            return Product.objects.get(slug=product_slug, is_published=True)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, product_slug, format=None):
        product = self.get_object( product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    

class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.order_by("-date_added")
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def get_categories(self, request):
        query = request.GET.get('search', '')
        if query:
            return self.search_categories(query)
        else:
            return Category.objects.order_by("-date_added")

    def search_categories(self, query):
        # Фильтруем категории по названию или другому атрибуту
        return Category.objects.filter(name__icontains=query).order_by("-date_added")


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    

class CategoryUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        # Возвращаем все категории программ пользователя
        programs = Category.objects.filter(owner=user)
        serializer = CategorySerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        if user:
            # Извлекаем данные для создания новой программы
            products_data = request.data.get('products', [])
            serializer = CategorySerializer(data=request.data, partial=True)

            if serializer.is_valid():
                new_category = serializer.save(owner=user)  # Указываем владельца
                # Если есть данные продуктов, создаем их
                if products_data is not None:
                    for product_data in products_data:
                        # Мы можем также использовать bulk_create для повышения производительности
                        Product.objects.create(category=new_category, **product_data)

                return Response(CategorySerializer(new_category).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "У вас нет прав для создания категории."}, status=status.HTTP_403_FORBIDDEN)


class DetailCategoryUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug, format=None):
        user = request.user
        try:
            category = Category.objects.get(slug=slug, owner=user)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            return Response({'error': 'Программа не найдена или вы не имеете права её просматривать.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug, format=None):
        user = request.user

        try:
            category = Category.objects.get(slug=slug, owner=user)

        except Category.DoesNotExist:
            return Response({'error': 'Программа не найдена или вы не имеете права её редактировать.'}, status=status.HTTP_404_NOT_FOUND)

        # Создаем изменяемую копию данных
        data = request.data.copy()
        # Извлекаем продукты из изменяемых данных
        products_data = data.pop('products', None) 

        # Сериализуем измененные данные
        serializer = CategorySerializer(category, data=data, partial=True)

        if serializer.is_valid():
            updated_category = serializer.save()

            # Обновляем или создаём продукты
            if products_data is not None:
                # Очищаем старые продукты
                updated_category.products.all().delete()  

                for product_data in products_data:
                    Product.objects.create(category=updated_category, **product_data)
            return Response(CategorySerializer(updated_category).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, slug, format=None):
        user = request.user
        try:
            category = Category.objects.get(slug=slug, owner=user)
            category.delete()
            return Response({'message': 'Программа успешно удалена.'}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist:
            return Response({'error': 'Программа не найдена или вы не имеете права её удалять.'}, status=status.HTTP_404_NOT_FOUND)
        

class ProductUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        products = Product.objects.filter(category__owner=user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        user = request.user
        # Получаем ID категории из запроса
        category_id = request.data.get('category_id')
        try:
            category = Category.objects.get(id=category_id, owner=user)
            serializer = ProductSerializer(data=request.data, partial=True)

            if serializer.is_valid():
                # Создаем продукт и связываем его с категорией
                serializer.save(category=category)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Product.DoesNotExist:
            return Response({'error': 'Пост не найден или вы не имеете доступа к нему.'}, status=status.HTTP_404_NOT_FOUND)


class DetailProductUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, slug, format=None):
        try:
            products = Product.objects.get(slug=slug)
            print(products, 'products')
            serializer = ProductSerializer(products)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Программа не найдена или вы не имеете права её просматривать.'}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, slug, format=None):
        try:
            product = Product.objects.get(slug=slug)
            serializer = ProductSerializer(product, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            return Response({'error': 'Пост не найден или у вас нет прав доступа.'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, slug, format=None):
        try:
            product = Product.objects.get(slug=slug)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден или у вас нет прав доступа.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({'products':[]})


class FavoriteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получаем все избранные продукты для данного пользователя
        favorites = FavoriteProduct.objects.filter(user=request.user)
        serializer = FavoriteProductSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Логика добавления в избранное
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        favorite_product, created = FavoriteProduct.objects.get_or_create(user=request.user, product_id=product_id)

        if created:
            return Response({"message": "Product added to favorites."}, status=status.HTTP_201_CREATED)
        return Response({"message": "Product already in favorites."}, status=status.HTTP_200_OK)  # Измените статус на 200

    def delete(self, request):
        # Логика удаления из избранного
        product_id = request.data.get("product_id")
        if not product_id:
            return Response({"error": "Product ID not provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            favorite_product = FavoriteProduct.objects.get(user=request.user, product_id=product_id)
            favorite_product.delete()
            return Response({"message": "Product removed from favorites."}, status=status.HTTP_204_NO_CONTENT)
        except FavoriteProduct.DoesNotExist:
            return Response({"error": "Product not found in favorites."}, status=status.HTTP_404_NOT_FOUND)

