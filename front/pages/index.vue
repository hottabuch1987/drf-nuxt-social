<template>
  <section class="relative bg-gradient-to-br from-orange-400 to-indigo-400 text-white overflow-hidden">
    <div v-if="isLoading">
      <!-- Спиннер -->
      <div aria-label="Loading..." role="status" class="flex items-center space-x-2">
        <svg class="h-20 w-20 animate-spin stroke-gray-500" viewBox="0 0 256 256">
          <line x1="128" y1="32" x2="128" y2="64" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="195.9" y1="60.1" x2="173.3" y2="82.7" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="224" y1="128" x2="192" y2="128" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="195.9" y1="195.9" x2="173.3" y2="173.3" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="128" y1="224" x2="128" y2="192" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="60.1" y1="195.9" x2="82.7" y2="173.3" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="32" y1="128" x2="64" y2="128" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
          <line x1="60.1" y1="60.1" x2="82.7" y2="82.7" stroke-linecap="round" stroke-linejoin="round" stroke-width="24"></line>
        </svg>
        <span class="text-4xl font-medium text-gray-500">Загрузка...</span>
      </div>
    </div>

    <div v-else>
      <div class="absolute inset-0 bg-black opacity-50">
        <h1 class=""></h1>
      </div>
      <img class="absolute inset-0 w-full h-full object-cover object-center blur" src="@/assets/img/home.jpg" alt="index">
    
      <div class="container mx-auto px-4 py-4 md:py-32 relative">
        <div class="flex flex-col md:flex-row items-center justify-between">
          <!-- Левая сторона: Информация о компании -->
          <div class="w-full md:w-1/2 mb-12 md:mb-0">
            <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Знакомства <br>Общение
            </h1>
            <template v-if="userStore.user.isAuthenticated && userStore.user.id">
              <p class="text-xl mb-8 text-gray-300">Добро пожаловать {{ userStore.user.username }}</p>
              <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <nuxt-link to="/posts"
                  class="border-2 border-white text-white font-semibold px-8 py-3 rounded-full hover:bg-white hover:text-blue-900 transition duration-300 text-center">Все Посты
                </nuxt-link>
              </div>
            </template>

            <template v-else>
              <p class="text-xl mb-8 text-gray-300">Регистрируйтесь или войдите </p>
              <div class="flex flex-col sm:flex-row space-y-4 sm:space-y-0 sm:space-x-4">
                <nuxt-link class="bg-white text-blue-900 font-semibold px-8 py-3 rounded-full hover:bg-blue-100 transition duration-300 text-center" :to="{ name: 'login' }">
                  Войти
                </nuxt-link>
                <nuxt-link to="/signup"
                  class="border-2 border-white text-white font-semibold px-8 py-3 rounded-full hover:bg-white hover:text-blue-900 transition duration-300 text-center">Регистрация
                </nuxt-link>
              </div>
            </template>
          </div>

          <!-- Правая сторона: Особенности -->
          <div class="w-full md:w-1/2 md:pl-12">
            <div class="bg-white bg-opacity-10 backdrop-filter backdrop-blur-lg rounded-xl p-8 shadow-2xl">
              <h2 class="text-2xl font-semibold mb-6">Что тебя ждет?</h2>
              <ul class="space-y-4">
                <li class="flex items-center">
                  <svg class="w-6 h-6 mr-3 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  <span>Размещай свои посты</span>
                </li>
                <li class="flex items-center">
                  <svg class="w-6 h-6 mr-3 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                  <span>Общайтесь с друзьями</span>
                </li>
                <li class="flex items-center">
                  <svg class="w-6 h-6 mr-3 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path></svg>
                  <span>Знакомьтесь в личной переписке</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Декоративный элемент -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg viewBox="0 0 1440 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M0 120L60 105C120 90 240 60 360 45C480 30 600 30 720 37.5C840 45 960 60 1080 67.5C1200 75 1320 75 1380 75L1440 75V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0Z" fill="white"/>
        </svg>
      </div>
    </div>
  </section>
</template>

<script>
import { useUserStore } from '@/stores/user';
import axios from 'axios';
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const userStore = useUserStore();
    const isLoading = ref(true);  // Создаем реактивное свойство для состояния загрузки

    const init = async () => {
      await userStore.initStore();

      const token = userStore.user.access;
      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
      } else {
        axios.defaults.headers.common['Authorization'] = '';
      }

      isLoading.value = false; // Устанавливаем состояние загрузки в false после загрузки
    };
    onMounted(() => {

        document.title = "Главная | Poster";

        init(); // Начинаем загрузку данных после монтирования

      });
  

    return {
      userStore,
      isLoading,
    };
  },
};
</script>

<style>
.blur {
  filter: blur(3px); /* Измените значение (3px) по мере необходимости */
}
</style>
