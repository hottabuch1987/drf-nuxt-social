<template>
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold text-gray-600 mb-4" v-if="favorites.length">Избранное </h1>
      <div v-if="loading" class="text-center text-gray-500">Загрузка...</div>
      <div v-else>
        <ul class="space-y-4">
          <li v-for="product in favorites" :key="product.product.id" class="flex justify-between items-center bg-white shadow-md rounded-lg p-4 hover:shadow-lg transition-shadow">
          
            <nuxt-link 
                  :to="`/posts/${product.product.slug}/`" 
                  class="text-lg font-semibold text-gray-500"
                >
                  {{ product.product.name }}
                </nuxt-link>
            <button class="mt-2 bg-red-400 hover:bg-red-600 text-white font-bold py-2 px-4 rounded transition-colors" @click="removeFromFavorites(product.product.id)">
              Удалить
            </button>
          </li>
        </ul>
      </div>
      <div v-if="!favorites.length" class="mt-4 text-center text-gray-600">Нет избранных постов.</div>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  import { useUserStore } from '@/stores/user';
  import { useToastStore } from '@/stores/toast';

  export default {
    name: 'FavoritePage',
    setup() {
        const userStore = useUserStore();
        const toastStore = useToastStore();
        return { userStore, toastStore };
    },
    data() {
      return {
        favorites: [],
        loading: true,
      };
    },
    async mounted() {
      await this.fetchFavorites();
    },
    methods: {
      async fetchFavorites() {
        try {
          const response = await axios.get('/favorites/'); // Вызов API для получения избранных
          this.favorites = response.data;
        } catch (error) {
          console.error('Ошибка при получении избранных продуктов:', error);
        } finally {
          this.loading = false;
        }
      },
      async removeFromFavorites(productId) {
        try {
          await axios.delete('/favorites/', {
            data: { product_id: productId, user: useUserStore().user.id }, // Указываем ID продукта для удаления
          });
          this.toastStore.showToast(5000, 'Товар удален из избранного!', 'bg-green-500');
          // После успешного удаления повторно загрузим избранные продукты
          await this.fetchFavorites();
        } catch (error) {
          console.error('Ошибка при удалении из избранных:', error);
          this.toastStore.showToast(5000, 'Произошла ошибка при удалении из избранного!', 'bg-green-500');
        }
      },
    },
  };
  </script>
  

  