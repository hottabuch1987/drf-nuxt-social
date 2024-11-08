<template>
    <div>
      <h1>Избранные</h1>
      <div v-if="loading">Загрузка...</div>
      <div v-else>
        <ul v-if="favorites.length">
          <li v-for="product in favorites" :key="product.product.id">
            {{ product.product.name }}
            <button @click="removeFromFavorites(product.product.id)">Удалить из избранного</button>
          </li>
        </ul>
        <div v-else>Нет избранных постов.</div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    name: 'FavoritePage',
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
            data: { product_id: productId }, // Указываем ID продукта для удаления
          });
          // После успешного удаления повторно загрузим избранные продукты
          await this.fetchFavorites();
        } catch (error) {
          console.error('Ошибка при удалении из избранных:', error);
        }
      },
    },
  };
  </script>
  

  