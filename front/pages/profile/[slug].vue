<template>
  <div class="max-w-lg mx-auto bg-white dark:bg-gray-900 rounded-lg overflow-hidden shadow-lg" v-if="user">
    <div class="px-4 py-6">
      <div class="text-center my-4">
        <img 
          class="h-72 w-72 rounded-full border-4 border-white dark:border-gray-800 mx-auto my-4"
          v-if="user.photos && user.photos.length > 0 && user.photos[user.photos.length - 1].get_image"
          :src="user.photos[user.photos.length - 1].get_image"
          alt="User Photo"
          @click="openModal"
        />
        <img 
          class="h-32 w-32 rounded-full border-4 border-white dark:border-gray-800 mx-auto my-4"
          v-else
          src="https://cdn-icons-png.flaticon.com/512/149/149071.png"
          alt="Avatar User"
        />
        
        <div class="py-2">
          <h3 class="font-bold text-2xl text-gray-600 dark:text-white mb-1">{{ user.username }}</h3>
          <h5 class="font-light text-2xl text-gray-600 dark:text-white mb-1">{{ user.first_name }} {{ user.last_name }}</h5>
          <p v-if="user.birth_date">
            <span class="text-gray-600 font-bold">{{ formatDate(user.birth_date) }}</span>
          </p>
          <p v-if="user.bio">
            <span class="text-gray-600 font-bold">{{ user.bio }}</span>
          </p>
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

  <!-- Модальное окно с каруселью фотографий -->
  <!-- Модальное окно с каруселью фотографий -->
<div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70" @click.self="closeModal">
  <div class="relative bg-white p-5 rounded shadow-lg max-w-md">
    <button @click="closeModal" class="absolute top-2 right-2 text-gray-600 hover:text-gray-900">✖</button>
    
    <h2 class="text-xl font-bold text-center">Все фотографии пользователя</h2>
    <div class="flex items-center justify-between mt-4">
      <button 
        @click="prevPhoto" 
        class="px-2 py-1 bg-gray-300 rounded" 
        v-if="currentPhotoIndex > 0">←</button>

      <img 
        v-if="user.photos[currentPhotoIndex]" 
        :src="user.photos[currentPhotoIndex].get_image" 
        alt="User Photo" 
        class="w-full object-cover mb-2"
      />

      <button 
        @click="nextPhoto" 
        class="px-2 py-1 bg-gray-300 rounded" 
        v-if="currentPhotoIndex < user.photos.length - 1">→</button>
    </div>
  </div>
</div>

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
      directId: null,
      isModalOpen: false,
      currentPhotoIndex: 0, // Состояние для текущего индекса фото
    };
  },
  async mounted() {
    await this.getUser(this.$route.params.slug);
    await this.dialogUser();
  },
  methods: {
    openModal() {
      this.isModalOpen = true;
      this.currentPhotoIndex = 0; // Сброс индекса при открытии
    },
    
    closeModal() {
      this.isModalOpen = false;
    },
    
    prevPhoto() {
      if (this.currentPhotoIndex > 0) {
        this.currentPhotoIndex -= 1;
      }
    },

    nextPhoto() {
      if (this.currentPhotoIndex < this.user.photos.length - 1) {
        this.currentPhotoIndex += 1;
      }
    },
  
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
        const response = await axios.get('/dialogs');
        const myDialogs = response.data;
        this.dialogs = myDialogs.filter(dialog => 
          dialog.user1.id === this.user.id || dialog.user2.id === this.user.id
        );
        this.hasDialog = this.dialogs.length > 0;
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
        this.directId = response.data.id;
        this.hasDialog = true;
        this.toastStore.showToast(5000, 'Диалог успешно создан!', 'bg-green-500');
      } catch (error) {
        console.error("Error creating dialog:", error);
      }
    },
  },
};
</script>

<style>
/* Добавьте базовые стили для карусели по вашему усмотрению */
</style>
