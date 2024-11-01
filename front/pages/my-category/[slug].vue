<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
    <div class="text-center p-6">
      <h1 class="font-bold text-4xl text-gray-600 mb-4">
        {{ isEditing ? "Редактировать категорию" : category.name }}
      </h1>
      <img
        v-if="!isEditing && category.get_image"
        :src="category.get_image"
        alt="Category Image"
        class="rounded-lg mb-6 object-cover h-48 w-full"
      />
    </div>

    <Spinner v-if="isLoading" />

    <section v-else class="p-6">
      <form v-if="isEditing" @submit.prevent="submitEdit">
        <div class="mb-4">
          <label class="block text-gray-700 font-medium">Название</label>
          <input
            v-model="editCategory.name"
            type="text"
            required
            class="border border-gray-300 rounded p-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label class="block text-gray-700 font-medium" for="avatar">Изображение</label>
          <div v-if="editCategory.imageURL">
            <img :src="editCategory.imageURL" alt="Current Image" class="rounded-lg mb-4 object-cover h-48 w-full" />
          </div>
          <input
            type="file"
            @change="handleFileUpload"
            accept="image/*"
            class="border border-gray-300 rounded p-2 w-full"
          />
        </div>

        <div class="mb-4">
          <label class="inline-flex items-center">
            <input
              type="checkbox"
              v-model="editCategory.is_published"
              class="mr-2"
            />
            <span>Опубликовать</span>
          </label>
        </div>

        <div class="flex justify-between">
          <button type="submit" class="bg-blue-500 text-white p-2 rounded hover:bg-blue-600 transition">
            Сохранить изменения
          </button>
          <button
            @click.prevent="isEditing = false"
            class="bg-gray-500 text-white p-2 rounded ml-2 hover:bg-gray-600 transition"
          >
            Отменить
          </button>
        </div>
      </form>

      <div v-else>
        <p class="text-gray-500">
          <strong>Статус:</strong>
          {{ category.is_published ? "Опубликовано" : "Не опубликовано" }}
        </p>

        <h2 class="text-2xl text-gray-600 font-bold mt-10">Продукты</h2>
        
        <div class="text-gray-400" v-if="!category.products.length">Нет продуктов в этой категории.</div>
        <button
          @click="isEditing = true"
          class="mt-4 bg-yellow-500 text-white p-2 rounded hover:bg-yellow-600 transition"
        >
          Редактировать категорию
        </button>

        <div class="mt-4">
          <p class="font-bold text-gray-700">Список продуктов:</p>
          <ul class="list-disc mt-2 pl-4">
            <li v-for="product in category.products" :key="product.id">
              <nuxt-link :to="`/my-product/${product.slug}/`" class="font-bold text-red-600 hover:text-red-800 transition">{{ product.name }}</nuxt-link>
            </li>
          </ul>
        </div>
        
        <nuxt-link :to="`/my-product/`" class="block mt-4 ml-2 font-bold text-red-600 hover:text-red-800 transition">Создать новый</nuxt-link>
      </div>
    </section>
  </div>
</template>


<script>
import axios from 'axios';
import Spinner from '@/components/Spinner.vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  components: {
    Spinner,
  },
  data() {
    return {
      category: {},
      editCategory: {
        name: '',
        is_published: false,
        image: null, // Для хранения загруженного изображения
        imageURL: '', // Для безопасного отображения URL изображения
      },
      isLoading: true,
      isEditing: false,
      toastStore: useToastStore(),
    };
  },
  async mounted() {
    const slug = this.$route.params.slug; // Получаем slug из параметров маршрута
    await this.getCategory(slug);
    this.setOwner();
  },
  methods: {
    setOwner() {
      const userStore = useUserStore();
      if (userStore.user && userStore.user.id) {
        this.editCategory.owner = userStore.user.id;
      } else {
        console.error("Пользователь не найден или не имеет ID");
      }
    },
    async getCategory(slug) {
      this.isLoading = true;
      try {
        const response = await axios.get(`/my-category/${slug}/`);
        this.category = response.data;
        this.editCategory = {
          name: this.category.name, // Предполагается наличие этого поля
          is_published: this.category.is_published,
          imageURL: this.category.get_image || '', // Сохраняем URL существующего изображения
        };
      } catch (error) {
        console.error('Ошибка при загрузке категории:', error);
      } finally {
        this.isLoading = false;
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.editCategory.image = file; // Сохраняем загруженное изображение
        // Создаем объект URL для отображения
        this.editCategory.imageURL = URL.createObjectURL(file);
      }
    },
    async submitEdit() {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("name", this.editCategory.name);
      formData.append("is_published", this.editCategory.is_published);

      // Проверяем, есть ли изображение, перед добавлением в FormData
      if (this.editCategory.image) {
        formData.append("image", this.editCategory.image);
      }

      try {
        const response = await axios.put(
          `/my-category/${this.category.slug}/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        this.category = response.data; // Обновляем категорию
        this.isEditing = false; // Закрываем форму редактирования
        this.toastStore.showToast(5000, 'Категория успешно изменена!', 'bg-emerald-500');
        
      } catch (error) {
          console.error("Ошибка при обновлении категории:", error);
          this.toastStore.showToast(5000, 'Ошибка при изменении категории!', 'bg-red-500'); 
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
