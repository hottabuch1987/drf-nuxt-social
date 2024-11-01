<template>
  <header class="flex flex-wrap items-center py-4 shadow-sm">
    <button @click="toggleMenu" class="lg:px-16 px-4 pointer-cursor md:hidden block">
      <svg class="fill-current text-gray-600" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20">
        <title>menu</title>
        <path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"></path>
      </svg>
    </button>

    <div :class="{ 'hidden md:flex md:items-center md:w-auto w-full': !isMenuOpen }" id="menu">
      <nav class="lg:px-16 px-4 flex flex-wrap items-center shadow-sm fixed top-0 w-full z-10 bg-white">
        <ul class="md:flex items-center justify-between text-base text-orange-500 pt-4 md:pt-0">
          <li @click="closeMenu">
            <nuxt-link class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]" :to="{ name: 'index' }">Главная</nuxt-link>
          </li>
          <li @click="closeMenu">
            <nuxt-link class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]" :to="{ name: 'trening' }">Объявления</nuxt-link>
          </li>
          <li @click="closeMenu">
            <nuxt-link class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]" :to="{ name: 'profile' }">Пользователи</nuxt-link>
          </li>
          <li @click="closeMenu">
            <nuxt-link to="/about" class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]">О нас</nuxt-link>
          </li>
          <template v-if="userStore.user.isAuthenticated"> 
            <!--userStore.user.isAuthenticated  && userStore.user.id -->
            <li @click="closeMenu">
              <nuxt-link to="/account" class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]">Профиль</nuxt-link>
            </li>
          </template>
          <template v-else>
            <li @click="closeMenu">
              <nuxt-link to="/login" class="md:p-4 py-3 px-3 block transition-transform duration-200 ease-in-out hover:scale-[1.05]">Войти</nuxt-link>
            </li>
          </template>
        </ul>
      </nav>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue';
import { useUserStore } from '@/stores/user';
import axios from 'axios';

export default {
  setup() {
    const userStore = useUserStore();
    const isMenuOpen = ref(false);

    function toggleMenu() {
      isMenuOpen.value = !isMenuOpen.value;
    }

    function closeMenu() {
      isMenuOpen.value = false;
    }

    return {
      userStore,
      isMenuOpen,
      toggleMenu,
      closeMenu
    };
  },

  mounted() {
    if (typeof window !== 'undefined') {
      this.userStore.initStore();

      const token = this.userStore.user.access;

      if (token) {
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;
      } else {
        axios.defaults.headers.common['Authorization'] = '';
      }
    }
  }
};
</script>
