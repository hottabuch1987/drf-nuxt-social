<template>
  <div class="max-w-md mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
    <div class="text-center p-6">
      <h1 class="font-bold text-3xl text-gray-600 mb-4">
         {{ isEditing ? "Редактировать категорию" : "категория " + category.name }}
      </h1>
      
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

       


        <div class="flex justify-between">
          <button type="submit" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">
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
        
        <button
          @click="isEditing = true"
          class="mt-4 bg-green-500 text-white p-2 rounded hover:bg-green-600 transition"
        >
          Редактировать категорию
        </button>

        <div class="mt-4 p-4 bg-gray-100 rounded-lg shadow-md">
          <p class="font-bold text-gray-700 text-lg">Список постов:</p>
          
          <div class="text-gray-400 mt-2" v-if="!category.products.length">Нет постов в этой категории.</div>
          
          <ul class="list-disc mt-2 pl-6 text-gray-600 space-y-1" v-for="product in category.products" :key="product.id">
            <nuxt-link :to="`/my-product/${product.slug}/`"  class="font-bold text-red-600 hover:text-red-800 transition"> 
            <li  class="hover:bg-gray-200 rounded p-2 transition">
                {{ product.name }}
            </li>
          </nuxt-link>
          </ul>
        </div>
        
        
        <nuxt-link :to="`/my-product/`" class="mt-4 bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">Создать новый пост</nuxt-link>
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
    
        };
      } catch (error) {
        console.error('Ошибка при загрузке категории:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async submitEdit() {
      this.isLoading = true;
      const formData = new FormData();
      formData.append("name", this.editCategory.name);


      // Проверяем, есть ли изображение, перед добавлением в FormData
      

      try {
        const response = await axios.put(
          `/my-category/${this.category.slug}/`,
          formData,
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
