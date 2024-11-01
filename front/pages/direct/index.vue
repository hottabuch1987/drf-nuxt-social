<template>
  <div class="container mx-auto p-4">
    <div class="max-w-4xl mx-auto bg-white rounded-lg overflow-hidden shadow-lg">
      <div class="md:flex bg-blue-100">
        <!-- Форма фильтрации -->
        <div class="w-full md:w-1/3 px-4 py-8 border-r border-gray-200">
          <h2 class="text-2xl text-gray-400 font-semibold mb-4">Фильтры</h2>
          <div class="mb-4">
            <label class="inline-flex items-center text-gray-400">
              <input type="radio" v-model="statusOrdering" value="created_at" @change="updateFilter" class="mr-2" name="statusOrder">
              Последние
            </label>
            <label class="inline-flex items-center ml-4 text-gray-400">
              <input type="radio" v-model="statusOrdering" value="-created_at" @change="updateFilter" class="mr-2" name="statusOrder">
              Все
            </label>
          </div>
        </div>

        <!-- Список сообщений -->
        <div class="w-full md:w-2/3 px-4 py-8">
          <h2 class="text-2xl text-gray-400 font-semibold mb-4">Мои диалоги</h2>
          <ul>
            <template v-if="dialogs.length === 0">
              <li class="py-4 text-gray-500">Нет сообщений.</li>
            </template>

            <template v-else>
              <div v-for="dialog in dialogs" :key="dialog.id" class="py-4 flex items-center justify-between">

              <div class="font-medium">
                <nuxt-link :to="`/profile/${dialog.user1.username}`" class="text-blue-600 hover:underline">
                  {{ dialog.user1.username === userStore.user.username ? 'Вы ' : dialog.user1.username }} 
                </nuxt-link> 
                <span class="mx-2"> </span> 

                <nuxt-link :to="`/profile/${dialog.user2.username}`" class="text-blue-600 hover:underline">
                  {{ dialog.user2.username === userStore.user.username ? '  Вам' : dialog.user2.username }}
                </nuxt-link>

              </div>
              <button @click="deleteDialog(dialog.id)" class="flex items-center text-red-400 text-sm hover:text-red-700">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M10 0a1 1 0 00-1 1v1H5a1 1 0 00-1 1v1h12V2a1 1 0 00-1-1h-4V0a1 1 0 00-1-1zM3 5v1h14V5H3zm4 3a1 1 0 00-.293.707v7a1 1 0 001 1h2a1 1 0 001-1v-7a1 1 0 00-.293-.707L10 8H7zm4-1.414A2 2 0 0010 5.586 2 2 0 009 7h3zM4 8h2a1 1 0 011 1v7a1 1 0 01-1 1H4a1 1 0 01-1-1v-7a1 1 0 011-1zm16 0h-2a1 1 0 00-1 1v7a1 1 0 001 1h2a1 1 0 001-1v-7a1 1 0 00-1-1zm-12 7h2v-5H8v5zm12-5h-2v5h2v-5z" />
                  </svg>
                  Удалить
                </button>
              <nuxt-link :to="`/direct/${dialog.id}`" class="bg-blue-600 text-white font-medium py-2 px-4 rounded-full hover:bg-blue-500">Написать</nuxt-link>

              </div>
            </template>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  data() {
    return {
      dialogs: [],
      statusOrdering: 'created_at', // Параметр для фильтрации
    };
  },

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return { userStore, toastStore };
  },

  mounted() {
    document.title = "Мои сообщения | Offer";
    this.fetchDialogs(); // Загружаем диалоги
  },

  methods: {
    async fetchDialogs() {
      // Получение диалогов по текущему фильтру
      try {
        const response = await axios.get('/dialogs', { params: { ordering: this.statusOrdering } });
        this.dialogs = response.data;
      } catch (error) {
        console.error('Ошибка при получении диалогов:', error);
      }
    },

    updateFilter() {
      // При изменении фильтра перезагружаем данные
      this.fetchDialogs();
    },
    async deleteDialog(id) {
      try {
        await axios.delete(`/dialogs/${id}`);
        this.dialogs = this.dialogs.filter(dialog => dialog.id !== id);
        this.toastStore.showToast(5000, 'Диалоги успешно удалены!', 'bg-green-500');
      } catch (error) {
        console.error('Error deleting dialog:', error);
      }
    }
  }
};
</script>





