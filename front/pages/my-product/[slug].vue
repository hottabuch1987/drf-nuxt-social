<template>
  <div class="max-w-2xl mx-auto p-10 bg-white rounded-lg shadow-md">
    <div class="text-center mb-6">
      <h1 class="font-bold text-4xl text-gray-400 mb-4">
        {{ isEditing ? "Редактировать пост" : product.name }}
      </h1>
      <div v-if="!product" class="text-gray-400 text-lg">Нет постов в этой категории.</div>
    </div>

    <Spinner v-if="isLoading" />

    <div v-else>
      <div class="relative rounded-md overflow-hidden shadow-md hover:shadow-lg" v-if="product">
        <img class="w-full object-cover h-64" :src="product.get_image" alt="Product Image" v-if="product.get_image" />
        <div v-if="product.get_image" class="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 m-2 rounded-md text-sm font-medium">
         {{ product.is_published ? 'Опубликован' : 'Не опубликован' }}
        </div>

        <div class="mt-4" v-if="product.get_video">
          <h4 class="font-medium text-lg">Видео инструкция</h4>
          <video class="w-full mt-2" controls>
            <source :src="product.get_video" type="video/mp4">
          </video>
        </div>
     
        <div class="p-4">
          <h3 class="text-lg font-bold text-gray-500 mb-2">{{ product.name }}</h3>
          <p class="text-gray-600 text-sm mb-4">{{ product.description }}</p>
        </div>
      </div>

      <section v-if="isEditing" class="mt-10 text-gray-400">
        <form @submit.prevent="submitEdit">
          <div class="mb-4">
            <label class="block text-gray-400 font-semibold">Название</label>
            <input
              v-model="editProduct.name"
              type="text"
              required
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="block text-gray-400 font-semibold">Описание</label>
            <input
              v-model="editProduct.description"
              type="text"
              required
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="block font-semibold">Изображение</label>
            <div v-if="editProduct.imageURL">
              <img :src="editProduct.imageURL" alt="Текущее изображение" class="rounded-lg mb-4" />
            </div>
            <input
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="block font-semibold">Видео</label>
            <div v-if="editProduct.videoURL">
              <video :src="editProduct.videoURL" controls class="rounded-lg mb-4"></video>
            </div>
            <input
              type="file"
              @change="handleVideoUpload"
              accept="video/*"
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="inline-flex items-center">
              <input
                type="checkbox"
                v-model="editProduct.is_published"
                class="mr-2"
              />
              <span>Опубликовать</span>
            </label>
          </div>

          <div class="flex justify-between mt-4">
            <button type="submit" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">
              Сохранить изменения
            </button>
            <button
              @click.prevent="isEditing = false"
              class="bg-gray-500 text-white p-2 rounded hover:bg-gray-600 transition"
            >
              Отменить
            </button>
          </div>
        </form>
      </section>

      <div class="flex justify-between mt-4">
        <button @click="deleteProduct(product)" class="text-red-600 hover:text-red-800">Удалить пост
          <!-- SVG для кнопки удаления -->
        </button>
        <button @click="isEditing = true" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">Редактировать пост</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Spinner from "@/components/Spinner.vue";
import { useToastStore } from '@/stores/toast';

export default {
  components: {
    Spinner,
  },
  data() {
    return {
      product: {},
      editProduct: {
        name: '',
        video: null,
        description: '',
        is_published: false,
        image: null,
        imageURL: "", // URL для отображения текущего изображения
        videoURL: "", // URL для отображения текущего видео
      },
      isLoading: true,
      isEditing: false,
      toastStore: useToastStore(),
    };
  },
  async mounted() {
    const slug = this.$route.params.slug; // Получаем slug из параметров маршрута
    await this.getProduct(slug);
  },
  methods: {
    async getProduct(slug) {
      this.isLoading = true;
      try {
        const response = await axios.get(`/my-product/${slug}/`);
        this.product = response.data;
        
        this.editProduct = {
          name: this.product.name,
          description: this.product.description,
          is_published: this.product.is_published,
          imageURL: this.product.get_image || "", // Сохраняем URL существующего изображения
          videoURL: this.product.get_video || "", // Сохраняем URL существующего видео
        };
      } catch (error) {
        console.error("Ошибка при загрузке поста:", error);
      } finally {
        this.isLoading = false;
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.editProduct.image = file; // Сохраняем загруженное изображение
        // Создаем объект URL для отображения
        this.editProduct.imageURL = URL.createObjectURL(file);
      }
      // Если файл не выбран, оставляем текущее изображение
    },

    handleVideoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Проверяем, является ли файл допустимым видеофайлом 
        this.editProduct.video = file; // Сохраняем загруженное видео
        // Создаем объект URL для отображения
        this.editProduct.videoURL = URL.createObjectURL(file);
      }
    },


    deleteProduct(product) {
      if (confirm(`Вы уверены, что хотите удалить пост "${product.name}"?`)) {
        this.isLoading = true;
        axios
          .delete(`/my-product/${product.slug}/`)
          .then(() => {
            this.product = null; // Продукт успешно удалён
            this.toastStore.showToast(5000, 'Пост успешно удален!', 'bg-green-500');
            this.$router.push({ name: 'my-product' });
          })
          .catch(error => {
            console.error('Ошибка при удалении Поста:', error);
            this.toastStore.showToast(5000, 'Ошибка при удалении Поста!', 'bg-red-500'); 
          })
          .finally(() => {
            this.isLoading = false;
          });
      }
    },

    
    async submitEdit() {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("name", this.editProduct.name);
      formData.append("is_published", this.editProduct.is_published);
      formData.append("description", this.editProduct.description);
      
      // Проверяем, есть ли изображение или видео, перед добавлением в FormData
      if (this.editProduct.image) {
        formData.append("image", this.editProduct.image);
      } 
      
      // Убедитесь, что video URL используется, если видео не загружено
      if (this.editProduct.video) {
        formData.append("video", this.editProduct.video);
      } 
      
      try {
        const response = await axios.put(
          `/my-product/${this.product.slug}/`,
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );
        this.product = response.data; // Обновляем продукт
        this.isEditing = false; // Закрываем форму редактирования
        this.toastStore.showToast(5000, 'Пост успешно обновлен!', 'bg-green-500');
      } catch (error) {
        console.error("Ошибка при обновлении Поста:", error);
        this.toastStore.showToast(5000, 'Ошибка при изменении Поста!', 'bg-red-500');
      } finally {
        this.isLoading = false;
      }
    }

  },
};
</script>

