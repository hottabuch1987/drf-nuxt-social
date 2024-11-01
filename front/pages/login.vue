<template>
  <main class="container mx-auto p-4 mt-12 bg-white flex flex-col items-center justify-center text-gray-700">
    <div class="w-10/12 sm:w-8/12 md:w-6/12 lg:w-5/12 xl:w-4/12 mb-4 ">
      <h1 class="text-4xl text-gray-400 font-semibold">Войти</h1>
    </div>
    <div class="w-10/12 sm:w-8/12 md:w-6/12 lg:w-5/12 xl:w-4/12 mb-6">
      <form class="space-y-6" v-on:submit.prevent="submitForm">
        <input
          type="email"
          v-model="form.email"
          class="mb-4 p-2 appearance-none block w-full bg-gray-200 placeholder-gray-400 rounded border focus:border-teal-500"
          placeholder="Email"
        />
        <input
          type="password"
          v-model="form.password"
          class="mb-4 p-2 appearance-none block w-full bg-gray-200 placeholder-gray-400 rounded border focus:border-teal-500"
          placeholder="Пароль"
        />

        <div class="flex items-center">
          

          <button class="ml-auto w-1/2 bg-gray-800 text-white p-2 m-2 rounded font-semibold hover:bg-gray-600" type="submit" :disabled="loading">
            Отправить
          </button>
          
          <nuxt-link
            to="/signup"
            class="rounded-md to-emerald-400 px-3 py-1.5 font-dm text-sm font-medium shadow-md transition-transform duration-200 ease-in-out hover:scale-[1.03]"
          >
            Регистрация
          </nuxt-link>
        </div>
      </form>
      
      <Spinner v-if="loading" />
        


      <template v-if="errors.length > 0">
        <div class="bg-red-300 text-white rounded-lg p-6">
          <p v-for="error in errors" :key="error">{{ error }}</p>
        </div>
      </template>
    </div>
  </main>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import Spinner from '@/components/Spinner.vue'; 

export default {
  name: 'login',
  components: {
    Spinner,
  },
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();

    return {
      userStore,
      toastStore,
    };
  },

  data() {
    return {
      form: {
        email: '',
        password: '',
      },
      errors: [],
      loading: false,
    };
  },

  mounted() {
    document.title = "Войти | Offer";
    this.checkToken();
  },

  methods: {
    async submitForm() {
      this.errors = [];
      this.loading = true; 

      if (this.form.email === '') {
        this.errors.push('Поле "E-mail" не может быть пустым!');
      }

      if (this.form.password === '') {
        this.errors.push('Поле "Пароль" не может быть пустым!');
      }

      if (this.errors.length === 0) {
        try {
          const response = await axios.post('/login/', this.form);
          this.userStore.setToken(response.data);
          axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;

          await this.fetchUserInfo(); // Получаем информацию о пользователе
        } catch (error) {
          console.log('Ошибка:', error);
          this.errors.push('Электронная почта или пароль неверны!');
        }
      }
      
      this.loading = false; // Завершение загрузки
    },

    async fetchUserInfo() {
      try {
        const response = await axios.get('/account/');
        this.userStore.setUserInfo(response.data);
        this.$router.push('/account');
        this.toastStore.showToast(5000, `${this.userStore.user.username}, Вы вошли в систему!`, 'bg-emerald-500');
      } catch (error) {
        console.log('Ошибка при получении информации о пользователе:', error);
      }
    },

    checkToken() {
      if (this.userStore.token) {
        this.$router.push('/account');
      }
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
