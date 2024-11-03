<template>
    <main class="container mx-auto p-4 mt-12 bg-white flex flex-col items-center justify-center text-gray-700">
      <div class="w-10/12 sm:w-8/12 md:w-6/12 lg:w-5/12 xl:w-4/12 mb-4">
        <h1 class="text-4xl text-gray-400 font-semibold">Активация аккаунта</h1>
      </div>
      <div class="w-10/12 sm:w-8/12 md:w-6/12 lg:w-5/12 xl:w-4/12 mb-6">
        <form class="space-y-6" @submit.prevent="submitForm">
          <input
            type="text"
            v-model="form.active_code"
            class="mb-4 p-2 block w-full bg-gray-200 placeholder-gray-400 rounded border focus:border-teal-500"
            placeholder="Код активации"
          />
  
          <div class="flex items-center">
            <button
              class="ml-auto w-1/2 bg-gray-800 text-white p-2 m-2 rounded font-semibold hover:bg-gray-600"
              type="submit"
              :disabled="loading"
            >
              Подтвердить
            </button>
  
            <nuxt-link
              to="/signup"
              class="rounded-md to-emerald-400 px-3 py-1.5 font-dm text-sm font-medium shadow-md transition-transform duration-200 ease-in-out hover:scale-[1.03]"
            >
              Регистрация
            </nuxt-link>
          </div>
  
          <div class="mt-4">
            <button
              v-if="canResend"
              class="bg-teal-500 text-white p-2 rounded"
              @click.prevent="resendCode"
            >
              Повторно отправить код
            </button>
            <span v-else>
              Код можно повторно отправить через {{ countdown }} секунд
            </span>
          </div>
        </form>
  
        <Spinner v-if="loading" />
  
        <template v-if="errors.length > 0">
          <div class="bg-red-300 text-white rounded-lg p-6 mt-4">
            <p v-for="(error, index) in errors" :key="index">{{ error }}</p>
          </div>
        </template>
      </div>
    </main>
  </template>

<script>
import axios from 'axios';
import { useToastStore } from '@/stores/toast';
import Spinner from '@/components/Spinner.vue';

export default {
  name: 'active-account',
  components: {
    Spinner,
  },
  setup() {
    const toastStore = useToastStore();

    return {
      toastStore,
    };
  },

  data() {
    return {
      form: {
        active_code: '',
      },
      errors: [],
      loading: false,
      canResend: true,
      countdown: 0,
      countdownInterval: null,
    };
  },

  mounted() {
    document.title = "Активация аккаунта | Poster";
    this.startCountdown();
  },

  beforeDestroy() {
    clearInterval(this.countdownInterval); // Очищаем таймер при уничтожении компонента
  },

  methods: {
    async submitForm() {
      this.errors = [];
      this.loading = true;

      if (!this.form.active_code) {
        this.errors.push('Поле "Код активации" не может быть пустым!');
      }

      if (this.errors.length === 0) {
        try {
          const response = await axios.post('/verify/', { 
            code: this.form.active_code,
          });

          if (response.data && response.data.message) {
            this.toastStore.showToast(5000, response.data.message, 'bg-emerald-500');
            this.$router.push('/login'); 
          } else {
            this.errors.push('Что-то пошло не так. Пожалуйста, попробуйте еще раз.');
          }
        } catch (error) {
          console.error('Ошибка:', error);
          this.handleResponseError(error.response);
        }
      }

      this.loading = false;
    },

    async resendCode() {
      this.loading = true;
      try {
        const response = await axios.post('/resend-code/', { 
          email: this.userEmail, // Передайте email или другой идентификатор для повторной отправки кода
        });

        if (response.data && response.data.message) {
          this.toastStore.showToast(5000, response.data.message, 'bg-emerald-500');
          this.resetCountdown(); // Сбрасываем таймер
        }
      } catch (error) {
        console.error('Ошибка:', error);
        this.errors.push('Не удалось отправить код повторно. Пожалуйста, попробуйте еще раз.');
      }
      this.loading = false;
    },

    startCountdown() {
      this.canResend = false;
      this.countdown = 60; // Установите продолжительность таймера
      this.countdownInterval = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.canResend = true;
          clearInterval(this.countdownInterval);
        }
      }, 1000);
    },

    resetCountdown() {
      this.countdown = 60; // Установите продолжительность таймера
      this.canResend = false;
      clearInterval(this.countdownInterval);
      this.startCountdown(); // Перезапускаем таймер
    },

    handleResponseError(response) {
      const { data } = response;
      if (data && data.message) {
        this.errors.push(data.message);
      } else {
        this.errors.push('Что-то пошло не так.');
      }
      this.toastStore.showToast(5000, 'Что-то пошло не так. Пожалуйста, попробуйте еще раз.', 'bg-red-300');
    },
  },
};
</script>

  