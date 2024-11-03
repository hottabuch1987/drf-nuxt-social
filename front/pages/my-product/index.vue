<template>
  <div>
    <div class="text-center p-10">
      <h1 class="text-4xl text-gray-400 font-semibold">Мои программы</h1>
      <button @click="showCreateForm = !showCreateForm" class="mt-4 p-2 bg-green-500 text-white rounded hover:bg-green-600 transition">
        {{ showCreateForm ? 'Отменить создание' : 'Создать пост' }}
      </button>
    </div>

    <Spinner v-if="isLoading" />

    <section
      v-else
      class="w-fit mx-auto grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 justify-items-center justify-center gap-y-20 gap-x-14 mt-10 mb-5"
    >
      <div class="text-gray-400" v-if="!products.length">Постов нет</div>

      <!-- Создание продукта -->
      <div v-if="showCreateForm" class="p-5 bg-gray-100 rounded">
        <h2 class="text-2xl font-bold text-gray-600">Создать пост</h2>

        <!-- Выбор категории -->
        <div class="mb-4">
          <label class="block text-gray-400">Выберите категорию</label>
          <select v-model="selectedCategoryId" class="border border-gray-300 rounded p-2 w-full" required>
            <option value="" disabled>Выберите категорию</option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
          </select>
        </div>

        <form @submit.prevent="submitProduct" enctype="multipart/form-data">
          <div class="mb-4">
            <label class="block text-gray-400">Название</label>
            <input v-model="newProduct.name" type="text" required class="border border-gray-300 rounded p-2 w-full" />
          </div>

          <div class="mb-4">
            <label class="block text-gray-400">Описание</label>
            <textarea v-model="newProduct.description" required class="border border-gray-300 rounded p-2 w-full"></textarea>
          </div>

          <div class="mb-4">
            <label class="block text-gray-400" for="avatar">Изображение</label>
            <input type="file" @change="handleFileUpload" accept="image/*" class="border border-gray-300 rounded p-2 w-full" />
          </div>

          <div class="mb-4">
            <label class="block font-semibold">Видео</label>
            <input
              type="file"
              @change="handleVideoUpload"
              accept="video/*"
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4 text-gray-400">  
            <label class="inline-flex items-center">
              <input type="checkbox" v-model="newProduct.is_published" class="mr-2 " />
              <span>Опубликовать</span>
            </label>
          </div>

          <button type="submit" class="bg-green-500 text-white p-2 rounded">Создать</button>
        </form>
      </div>

      <!-- Вывод продуктов -->
      <div
        v-for="product in products"
        :key="product.id"
        class="w-72 bg-white shadow-md rounded-xl duration-500 hover:scale-105 hover:shadow-xl"
      >
        <img v-if="product.get_image" :src="product.get_image" alt="" class="h-80 w-72 object-cover rounded-t-xl" />

        <nuxt-link :to="`/my-product/${product.slug}/`" class="font-bold text-red-600">{{ product.name }}</nuxt-link>
        <div class="p-4">
          <p class="text-gray-500">{{ product.description }}</p>  
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from '@/components/Spinner.vue';
import { useToastStore } from '@/stores/toast';

export default {
  components: {
    Spinner,
  },
  data() {
    return {
      products: [], // Массив продуктов
      categories: [], // Массив категорий
      isLoading: true,
      showCreateForm: false,
      selectedCategoryId: null, // ID выбранной категории
      toastStore: useToastStore(),
      newProduct: {
        name: '',
        description: '',
        is_published: false,
        image: null, // Для хранения загружаемого изображения
        video: null, // Для хранения загружаемого видео
      },
    };
  },
  mounted() {
    this.getProducts();
    this.getCategories(); // Получаем категории при монтировании компонента
  },
  methods: {
    getProducts() {
      this.isLoading = true;
      axios
        .get('/my-products/')
        .then(response => {
          this.products = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке продуктов:', error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    
    getCategories() {
      this.isLoading = true;
      axios
        .get('/my-category/')
        .then(response => {
          this.categories = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке категорий:', error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },

    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.newProduct.image = file;
      }
    },
    
    handleVideoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.newProduct.video = file; // Сохраняем загружаемое видео
      }
    },

    submitProduct() {
      this.isLoading = true;
      const formData = new FormData();

      // Добавляем поля к FormData
      formData.append('name', this.newProduct.name);
      formData.append('description', this.newProduct.description);
      formData.append('is_published', this.newProduct.is_published);
      formData.append('category_id', this.selectedCategoryId); // Добавление ID категории

      if (this.newProduct.image) {
        formData.append('image', this.newProduct.image);
      }

      if (this.newProduct.video) {
        formData.append('video', this.newProduct.video); // Добавляем видео в formData
      }

      axios
        .post('/my-products/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then(response => {
          this.products.push(response.data);
          this.resetForm(); // Сбрасываем поля
          this.showCreateForm = false;
          this.toastStore.showToast(5000, 'Пост успешно создан!', 'bg-green-500');
        })
        .catch(error => {
          console.error('Ошибка при создании поста:', error);
          this.toastStore.showToast(5000, 'Ошибка при создании поста!', 'bg-red-500');
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    
    resetForm() {
      this.newProduct = {
        name: '',
        description: '',
        is_published: false,
        image: null,
        video: null, // Сбрасываем видео
      };

      this.selectedCategoryId = null; // Сброс выбора категории
    }
  },
};
</script>
