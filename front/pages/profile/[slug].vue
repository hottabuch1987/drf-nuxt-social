<template>
  <!-- Card start -->
  <div class="max-w-lg mx-auto bg-white dark:bg-gray-900 rounded-lg overflow-hidden shadow-lg" v-if="user">
    <div class="px-4 py-6">
      <div class="text-center my-4">
        <img 
          class="h-72 w-72 rounded-full border-4 border-white dark:border-gray-800 mx-auto my-4" 
          v-if="user.avatar"
          :src="user.avatar" 
          alt="Avatar User" 
        >
        <img 
          class="h-32 w-32 rounded-full border-4 border-white dark:border-gray-800 mx-auto my-4" 
          v-else 
          src="https://cdn-icons-png.flaticon.com/512/149/149071.png" 
          alt="Avatar User" 
        >
        <div class="py-2">
          <h3 class="font-bold text-2xl text-gray-600 dark:text-white mb-1">{{ user.username }}</h3>
          <h5 class="font-light text-2xl text-gray-600 dark:text-white mb-1">{{ user.first_name }} {{ user.last_name }}</h5>
          <p v-if="user.birth_date">
            <span class="text-gray-600 font-bold">{{ formatDate(user.birth_date) }}</span>
          </p>
          <p v-if="user.bio">
            <span class="text-gray-600 font-bold">{{ user.bio }}</span>
          </p>
          <div class="inline-flex text-gray-700 dark:text-gray-300 items-center" v-if="user.is_trainer">
            <svg 
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6 text-yellow-500"
            > 
              <path d="M12 .587l3.668 7.568 8.332 1.144-6.004 5.547 1.412 8.208L12 18.896l-7.408 3.883 1.412-8.208-6.004-5.547 8.332-1.144L12 .587z"/>
            </svg>
            Бизнес аккаунт
          </div>
        </div>
        <div v-if="hasDialog">
          <nuxt-link 
            v-if="userStore.user.id !== user.id"
            :to="`/direct/${directId}`" 
            class="mt-3 sm:mt-0 py-2 px-5 md:py-3 md:px-6 bg-blue-700 hover:bg-blue-600 font-bold text-white md:text-lg rounded-lg shadow-md"
          >
            Написать
          </nuxt-link>
        </div>
        <div v-else>
          <button 
            @click="createDialog" 
            class="mt-3 sm:mt-0 py-2 px-5 md:py-3 md:px-6 bg-green-700 hover:bg-green-600 font-bold text-white md:text-lg rounded-lg shadow-md"
          >
            Начать чат
          </button>
        </div>
      </div>
    </div>
  </div>
  <!-- Card end -->
</template>

<script>
import axios from "axios";
import { useUserStore } from '@/stores/user';
import { DateTime } from "luxon";
import { useToastStore } from '@/stores/toast';

export default {
  data() {
    return {
      user: null,
      dialogs: [],
      hasDialog: false,
      userStore: useUserStore(),  
      toastStore: useToastStore(),
      directId: null // Хранит ID актуального диалога

    };
  },
  async mounted() {
    await this.getUser(this.$route.params.slug);
    await this.dialogUser();
  },
  methods: {
    async getUser(slug) {
      try {
        const response = await axios.get(`/user/${slug}`);
        this.user = response.data;
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    },
    
    formatDate(date) {
      return DateTime.fromISO(date).toLocaleString(DateTime.DATE_MED);
    },
    
    async dialogUser() {
      try {
        // Проверка наличия диалогов
        const response = await axios.get('/dialogs');
        const myDialogs = response.data;

        this.dialogs = myDialogs.filter(dialog => 
          dialog.user1.id === this.user.id || dialog.user2.id === this.user.id
        );

        // Проверка наличия диалогов
        this.hasDialog = this.dialogs.length > 0;

        // Если диалоги существуют, устанавливаем ID первого диалога
        if (this.hasDialog) {
          this.directId = this.dialogs[0].id;
        }
      } catch (error) {
        console.error("Error fetching dialog data:", error);
      }
    },

    async createDialog() {
      try {
        const response = await axios.post('/dialogs/', {
          user2: this.user.id,
          user1: this.userStore.user.id
        });
        this.directId = response.data.id; // Обновите ID на созданный
        this.hasDialog = true; // Обновляем состояние наличия диалога
        this.toastStore.showToast(5000, 'Диалог успешно создан!', 'bg-green-500');
      } catch (error) {
        console.error("Error creating dialog:", error);
      }
    },
  },
};
</script>
