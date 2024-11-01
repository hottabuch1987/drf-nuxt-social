<template>
  <button @click="logout" class="flex items-center space-x-3 py-3 px-4 w-full leading-6 text-lg text-gray-600 focus:outline-none hover:bg-gray-100 rounded-md transition-transform duration-200 ease-in-out hover:scale-[1.01]">
     <svg class="w-7 h-7" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
            <path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2"></path>
            <path d="M9 12h12l-3 -3"></path>
            <path d="M18 15l3 -3"></path>
     </svg>
    <span>Выход</span>
  </button>
</template>

<script>
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import { useRouter } from 'vue-router';

export default {
  name: 'LogoutButton',
  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const router = useRouter();
    const logout = () => {
            userStore.removeToken(); // Очистка данных пользователя из хранилища
            toastStore.showToast(5000, 'Вы вышли из системы!', 'bg-green-500');
            router.push({ name: 'login' });
        }
  
    return {
        logout,
        userStore,
        toastStore,
    }
  }
};
</script>
