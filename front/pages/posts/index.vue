<template>
  <div>
    <div class="text-center p-10">
      <h1 class="text-4xl text-gray-400 font-semibold" v-if="categories.length">Все Категории</h1>
      <h1 class="text-4xl text-gray-400 font-semibold" v-else>Нет Постов</h1>
    </div>

    <Spinner v-if="isLoading" />

    <section
      v-else
      class="w-fit mx-auto grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 justify-items-center justify-center gap-y-20 gap-x-14 mt-10 mb-5"
    >
      <div
        id="Projects"
        v-for="cat in categories"
        :key="cat.id"
        class="w-72 bg-white shadow-md rounded-xl duration-500"
      >
        <a href="#" v-if="cat.products.length">
          <span class="text-gray-400 mr-3 uppercase text-xs">  Категория <strong>{{ cat.name }}</strong> </span>
          <span class="text-gray-400 mr-3 uppercase text-xs">
            {{ cat.owner_username === userStore.user.username ? 'Моя категория' : 'Разместил  ' + cat.owner_username }}
          </span>
          
          <div class="px-4 py-3 w-72">
            <span class="text-gray-400 mr-3 uppercase text-xs">Посты</span>
            <p class="text-lg font-bold text-black truncate block capitalize"></p>
            <div class="flex items-center" v-for="product in cat.products" :key="product.id">
              <p class="text-3xl font-semibold text-black cursor-auto my-3" v-if="product.is_published">

                <nuxt-link 
                  :to="`/posts/${product.slug}/`" 
                  class="inline-block font-bold text-gray-600 hover:text-gray-800 transition-transform duration-300"
                >
                  {{ product.name }}
                </nuxt-link>

              </p>
              <p class="text-3xl font-semibold text-gray-500 cursor-auto my-3" v-else>Нет постов</p>
              <div class="ml-auto">
                
                <nuxt-link v-if="product.is_published"  :to="`/posts/${product.slug}/`" class="bg-white border border-gray-300 hover:bg-gray-200 text-gray-500 font-bold py-2 px-4 rounded ">
                  Подробнее
                </nuxt-link>
                
              </div>
            </div>
          </div>
        </a>
        
      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from '@/components/Spinner.vue'; // Импортируем компонент спиннера
import { useUserStore } from '@/stores/user';

export default {
  components: {
    Spinner, // Регистрация компонента
  },
  data() {
    return {
      categories: [],
      isLoading: true, // Добавляем состояние загрузки
      userStore: useUserStore(),
    };
  },
  mounted() {
    this.getCategories();
    document.title = "Посты | Posts";
  },
  methods: {
    getCategories() {
      this.isLoading = true; // Устанавливаем isLoading в true перед началом запроса
      axios
        .get('/trening-category')
        .then(response => {
          this.categories = response.data;
          console.log(response.data);
        })
        .catch(error => {
          console.log('Ошибка при загрузке категорий:', error);
        })
        .finally(() => {
          this.isLoading = false; // Устанавливаем isLoading в false после получения данных
        });
    },
  },
};
</script>
