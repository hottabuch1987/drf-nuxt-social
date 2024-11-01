<template>
    <!-- Спиннер при загрузке -->
<Spinner v-if="loading" />
  <div class="w-full max-w-2xl mx-auto rounded-md overflow-hidden shadow-md hover:shadow-lg" v-if="cat">
    <div class="relative" v-if="cat.get_image">
      <img class="w-full" :src="cat.get_image" alt="Trening Image" />
      <div class="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 m-2 rounded-md text-sm font-medium">
        Количество {{ cat.quantity_day }} шт.
      </div>
    </div>
    <div class="mt-4" v-if="cat.get_video">
      <h4 class="font-medium text-lg">Видео инструкция</h4>
      <video v-if="cat.get_video" class="w-full mt-2" controls>
        <source :src="cat.get_video" type="video/mp4" />
      </video>
    </div>
    <div class="p-4">
      <h3 class="text-lg font-medium font-bold text-red-600 mb-2">{{ cat.name }}</h3>
      <p class="text-gray-600 text-sm mb-4" v-html="cat.description"></p>
      <div class="flex items-center justify-between">
        <span class="font-bold text-red-600 text-lg">{{ cat.price }} ₽</span>
        
        <nuxt-link class="text-gray-400 mr-3 uppercase text-xs hover:text-red-600" 
          :to="cat.owner_username === userStore.user.username ? '/my-product' : `/profile/${cat.owner_username}`">
          {{ cat.owner_username === userStore.user.username ? 'Мой продукт' : 'Разместил ' + cat.owner_username }}
        </nuxt-link>
        
        <!-- Кнопка для создания заказа с открытием формы оплаты -->
        <button v-if="cat.owner_username !== userStore.user.username && !loading" 
                @click="initiatePayment" 
                class="bg-sky-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
          Заказать
        </button>
      </div>

      <!-- Форма оплаты -->
      <div v-if="showPaymentForm" class="mt-4">
        <h3 class="text-lg font-bold text-gray-500">Введите данные карты</h3>
        <div id="card-element" class="border-gray-600 p-3 rounded-md w-148 h-54"></div>
        <button @click="handlePayment" 
                :disabled="loading" 
                class="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded mt-2">
          Оплатить {{ cat.price }} ₽
        </button>
        <div v-if="paymentError" class="text-red-500 mt-2">{{ paymentError }}</div>
      </div>

      <div class="flex items-center mt-4">
        <button @click="toggleLike" 
                class="flex items-center bg-gray-200 hover:bg-gray-300 text-black font-bold py-2 px-4 rounded">
          <svg v-if="cat.is_liked" xmlns="http://www.w3.org/2000/svg" fill="red" viewBox="0 0 24 24" class="w-6 h-6 mr-2">
            <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="w-6 h-6 mr-2">
            <path stroke="currentColor" stroke-width="2" d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/>
          </svg>
          <span v-if="cat.is_liked"></span>
          <span v-else></span>
          <span class="ml-2 font-medium">{{ cat.likes_count }} </span>
        </button>
      </div>

    
    </div>
  </div>


  
  <!-- <div class="w-full max-w-2xl mx-auto rounded-md" v-else>
    <Spinner v-if="loading" />
  </div> -->
</template>

<script>
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';
import { useUserStore } from '@/stores/user';
import Spinner from '@/components/Spinner.vue';
import { useRuntimeConfig } from '#app'; 


export default {
  components: {
    Spinner,
  },
  data() {
    return {
      cat: null,
      showPaymentForm: false,
      paymentError: null,
      stripe: null,
      elements: null,
      cardElement: null,
      loading: false,
    };
  },

  setup() {
    const userStore = useUserStore();
    const config = useRuntimeConfig();
    return { userStore, config };
  },
  async mounted() {
    await this.getUser(this.$route.params.slug);
  },
  methods: {
    async initializeStripe() {
      this.stripe = await loadStripe(this.config.public.stripeKey);
      this.elements = this.stripe.elements();
      this.cardElement = this.elements.create('card');
      this.cardElement.mount('#card-element');
    },
    
    async getUser(slug) {
      this.loading = true;
      try {
        const response = await axios.get(`/trening/${slug}/`);
        this.cat = response.data;

        // Проверка лайка
        const likedPosts = this.userStore.likedPosts;
        this.cat.is_liked = likedPosts.includes(this.cat.id);
      } catch (error) {
        console.error('Error fetching cat data:', error);
      } finally {
        this.loading = false;
      }
    },

    initiatePayment() {
      this.showPaymentForm = true; // Показываем форму оплаты
      this.paymentError = null; // Сброс ошибки
      this.initializeStripe(); // Инициализация Stripe здесь
    },

    async handlePayment() {
      this.loading = true; // начинаем загрузку
      const orderData = {
        product: this.cat.id,
        user: this.userStore.user.id
      };

      try {
        // Создание заказа
        const orderResponse = await axios.post('/orders/create/', orderData);
        const orderId = orderResponse.data.id;

        // Получение токена Stripe
        const { token, error } = await this.stripe.createToken(this.cardElement);

        if (error) {
          throw new Error(error.message);
        }

        // Отправка токена на сервер
        const paymentResponse = await axios.post('/payment/', {
          order_id: orderId,
          token: token.id
        });

        if (paymentResponse.status === 201) {
          alert('Платеж успешен!');
          this.showPaymentForm = false; // Скрыть форму оплаты
          this.$router.push({ path: '/account' }); // Перенаправление на страницу аккаунта
        }
      } catch (error) {
        this.paymentError = error.response ? error.response.data.error : error.message;
        console.error('Payment error:', this.paymentError);
      } finally {
        this.loading = false; // заканчиваем загрузку
      }
    },

    async toggleLike() {
      const slug = this.cat.slug;
      const url = `/trening/${slug}/likes/`;

      try {
        if (this.cat.is_liked) {
          await axios.delete(url, {
            data: { user_id: this.userStore.user.id }
          });
          this.cat.likes_count--;
          this.userStore.unlikePost(this.cat.id);
        } else {
          await axios.post(url, {
            user_id: this.userStore.user.id
          });
          this.cat.likes_count++;
          this.userStore.likePost(this.cat.id);
        }
        this.cat.is_liked = !this.cat.is_liked;
      } catch (error) {
        console.error('Error toggling like:', error);
      }
    }
  }
};
</script>
