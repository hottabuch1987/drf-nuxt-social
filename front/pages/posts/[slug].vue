<template>
    <!-- Спиннер при загрузке -->
<Spinner v-if="loading" />
  <div class="w-full max-w-2xl mx-auto rounded-md overflow-hidden shadow-md hover:shadow-lg" v-if="cat">
    <div class="relative" v-if="cat.get_image">
      <img class="w-full" :src="cat.get_image" alt="Trening Image" />
      <div class="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 m-2 rounded-md text-sm font-medium">
         {{ cat.name }} 
     
      </div>
    </div>
    <div class="mt-4" v-if="cat.get_video">
      <h4 class="font-medium text-lg">Видео инструкция</h4>
      <video v-if="cat.get_video" class="w-full mt-2" controls>
        <source :src="cat.get_video" type="video/mp4" />
      </video>
    </div>
    <div class="p-4">
      <h3 class="text-lg font-medium font-bold text-red-600 mb-2">    {{ cat.description }}</h3>
      <p class="text-gray-600 text-sm mb-4"></p>
      <div class="flex items-center justify-between">
        <button class="mt-4 bg-white border border-red-500 hover:bg-red-200 text-red-500 font-bold py-2 px-4 rounded" @click="addFromFavorites(cat.id)">В избранное</button>
       
        
        <nuxt-link class="text-gray-400 mr-3 uppercase text-xs hover:text-red-600" v-if="userStore.user.username"
          :to="cat.owner_username === userStore.user.username ? '/my-product' : `/profile/${cat.owner_username}`">
          {{ cat.owner_username === userStore.user.username ? 'Мой пост' : 'Разместил ' + cat.owner_username}}
        </nuxt-link>
        
        <!-- Кнопка для создания заказа с открытием формы оплаты -->
        <!-- <button v-if="cat.owner_username !== userStore.user.username && !loading" 
                @click="initiatePayment" 
                class="bg-sky-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Заказать
        </button> -->
      </div>

      <!-- Форма оплаты -->
      <!-- <div v-if="showPaymentForm" class="mt-4">
        <h3 class="text-lg font-bold text-gray-500">Введите данные карты</h3>
        <div id="card-element" class="border-gray-600 p-3 rounded-md w-148 h-54"></div>
        <button @click="handlePayment" 
                :disabled="loading" 
                class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mt-2">
          Оплатить {{ cat.price }} ₽
        </button>
        <div v-if="paymentError" class="text-red-500 mt-2">{{ paymentError }}</div>
      </div> -->

  

    
    </div>
  </div>


  
  <!-- <div class="w-full max-w-2xl mx-auto rounded-md" v-else>
    <Spinner v-if="loading" />
  </div> -->
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import Spinner from '@/components/Spinner.vue';
import { useRuntimeConfig } from '#app'; 


export default {
  components: {
    Spinner,
  },
  data() {
    return {
      cat: null,
  
    };
  },

  setup() {
    const userStore = useUserStore();
    const config = useRuntimeConfig();
    const toastStore = useToastStore();
    return { userStore, config, toastStore };
  },
  async mounted() {
    await this.getUser(this.$route.params.slug);
  },
  methods: {
   
    
    async getUser(slug) {
      this.loading = true;
      try {
        const response = await axios.get(`/trening/${slug}/`);
        this.cat = response.data;

        // Проверка лайка
       
      } catch (error) {
        console.error('Error fetching cat data:', error);
      } finally {
        this.loading = false;
      }
    },
    async addFromFavorites(id) {
      try {
        const response = await axios.post('/favorites/', { product_id: id, user: this.userStore.user.id });
        
        // Успешное добавление товара в избранное
        if (response.status === 201) {
          this.toastStore.showToast(5000, 'Товар добавлен в избранное!', 'bg-green-500');
        } else {
          // Если товар уже добавлен, обрабатываем сообщением
          this.toastStore.showToast(5000, 'Товар уже добавлен в избранное!', 'bg-green-500');
        }

      } catch (error) {
        if (error.response && error.response.status === 400) {
          // Обработка случая, когда не предоставлен ID товара
          this.toastStore.showToast(5000, 'Ошибка: ID товара не предоставлен.', 'bg-red-500');
        } else {
          // Другие ошибки
          console.error('Error adding to favorites:', error);
          this.toastStore.showToast(5000, 'Ошибка при добавлении в избранное.', 'bg-red-500');
        }
      }
    }

  }
};
</script>
