<template>
  <div>
    <div class="text-center p-10">
      <h1 class="text-4xl text-gray-400 font-semibold" v-if="categories.length">Все Объявления</h1>
      <h1 class="text-4xl text-gray-400 font-semibold" v-else>Нет Объявлений</h1>
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
        class="w-72 bg-white shadow-md rounded-xl duration-500 hover:scale-105 hover:shadow-xl"
      >
        <a href="#" v-if="cat.products.length">
          <span class="text-gray-400 mr-3 uppercase text-xs">  Название {{ cat.name }} </span>
          <span class="text-gray-400 mr-3 uppercase text-xs">
            {{ cat.owner_username === userStore.user.username ? 'Моя категория' : 'Разместил  ' + cat.owner_username }}
          </span>
          
          <img :src="cat.get_image" alt="Category" class="h-80 w-72 object-cover rounded-t-xl" />
          <div class="px-4 py-3 w-72">
            <span class="text-gray-400 mr-3 uppercase text-xs">Объявления</span>
            <p class="text-lg font-bold text-black truncate block capitalize"></p>
            <div class="flex items-center" v-for="product in cat.products" :key="product.id">
              <p class="text-3xl font-semibold text-black cursor-auto my-3" v-if="product.is_published">

                <nuxt-link 
                  :to="`/trening/${product.slug}/`" 
                  class="inline-block font-bold text-red-600 hover:text-red-800 transition-transform duration-300 transform hover:scale-150"
                >
                  {{ product.name }}
                </nuxt-link>

              </p>
              <p class="text-3xl font-semibold text-black cursor-auto my-3" v-else>Нет продуктов</p>
              <div class="ml-auto">
                
                <nuxt-link v-if="product.is_published"  :to="`/trening/${product.slug}/`" class="inline-block transition-transform duration-300 transform hover:scale-150">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    shape-rendering="geometricPrecision"
                    text-rendering="geometricPrecision"
                    image-rendering="optimizeQuality"
                    fill-rule="evenodd"
                    clip-rule="evenodd"
                    viewBox="0 0 512 485.963"
                    width="21"   
                    height="21" 
                  >
                    <path d="M273.559 171.532L17.064 151.724C7.717 151.002 0 159.413 0 168.785v148.393c0 9.372 7.704 17.783 17.064 17.06l256.495-19.807v.369l-35.318 100.959c-19.779 51.211 12.189 91.873 49.588 57.439l199.982-191.637c32.252-32.255 32.252-45.759 0-78.011L287.829 11.913c-36.273-32.432-69.367 6.228-49.588 57.436l35.318 100.962v1.221z" fill="red"/>
                  </svg>
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
    document.title = "Обьявления | Offer";
  },
  methods: {
    getCategories() {
      this.isLoading = true; // Устанавливаем isLoading в true перед началом запроса
      axios
        .get('/trening-category/')
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
