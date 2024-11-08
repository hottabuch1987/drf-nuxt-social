<template>
  <div class="max-w-6xl mx-auto p-4">
    <div class="text-2xl text-gray-400 font-semibold mb-4">Мои сообщения</div>
    <div class="h-screen flex flex-col">
      <div class="bg-gray-200 flex-1 overflow-y-scroll">
        <div v-for="msg in messages" :key="msg.id" class="px-2 py-2">
          <div class="flex items-center mb-4" v-if="msg.sender.id === userStore.user.id">
            <nuxt-link :to="`/profile/${msg.sender.username}`" class="ml-2 text-blue-600 hover:underline mr-2">Вы</nuxt-link>

            <div class="bg-white text-lg rounded-lg p-2 shadow max-w-sm">
              {{ msg.content }}
              <div class="text-gray-500 text-xs">{{ new Date(msg.timestamp).toLocaleString() }}</div>
            </div>
          </div>

          <div class="flex items-center justify-end mb-4" v-else>
            <div class="bg-blue-300 text-white text-lg rounded-lg p-2 shadow max-w-sm">
              {{ msg.content }}
              <div class="text-gray-500 text-xs">{{ new Date(msg.timestamp).toLocaleString() }}</div>
            </div>
            <div class="font-medium mr-2">
              <nuxt-link :to="`/profile/${msg.sender.username}`" class="ml-2 text-blue-600 hover:underline">{{ msg.sender.username }}</nuxt-link>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-gray-100 px-4 py-2">
        <div class="flex items-center">
          <textarea 
            class="w-full border rounded-full py-2 px-4 mr-2"
            v-model="newMessage"
            placeholder="Напишите сообщение...">
          </textarea>
          <button 
            class="bg-blue-300 hover:bg-blue-400 text-white font-medium py-2 px-4 rounded-full" 
            @click="sendMessage">  
            Отправить  
          </button>  
        </div>  
      </div>
    </div>
  </div>
</template>


<script>
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';
import axios from 'axios';

export default {
  data() {
    return {
      messages: [],
      newMessage: '',
      dialogId: null,
      socket: null, // Сохранение соединения с веб-сокетом
      notification: '',
    };
  },

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return { userStore, toastStore };
  },

  mounted() {
    document.title = "Диалог с пользователем | Poster"; // Устанавливаем заголовок страницы
    this.dialogId = this.$route.params.id; // Получаем ID диалога из параметров маршрута

    this.fetchMessages();
    this.connectWebSocket(this.dialogId);
  },

  beforeDestroy() {
    // Закрываем сокет при уничтожении компонента
    if (this.socket) {
      this.socket.close();
    }
  },

  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get(`/dialogs/${this.dialogId}/messages`); // Используем правильный dialogId
        this.messages = response.data;
      } catch (error) {
        console.error('Ошибка при получении сообщений:', error);
      }
    },

    connectWebSocket(dialogId) {
      // Подключение к веб-сокету
      this.socket = new WebSocket(`ws://localhost:8000/ws/chat/${dialogId}/`);

      this.socket.onmessage = (event) => {
          const data = JSON.parse(event.data);
          
          if (data.notification) {
              // Вы можете отобразить уведомление пользователю с помощью UI
              // alert(data.notification);  // Простой способ, можно улучшить!
              // this.notification = data.notification;
              this.toastStore.showToast(8000, data.notification, 'bg-green-500');
          } else {
              // Добавляем сообщение к текущим сообщениям
              this.messages.push({
                  content: data.message,
                  sender: { id: data.sender_id, username: data.sender_username }, // sender_username передается
                  timestamp: data.timestamp,
              });
          }
      };


      this.socket.onclose = (event) => {
        console.log('WebSocket closed:', event);
      };

      this.socket.onerror = (error) => {
        console.error('WebSocket error observed:', error);
      };
    },

    sendMessage() {
      if (this.newMessage.trim() === '' || this.socket.readyState !== WebSocket.OPEN) return;

      this.socket.send(JSON.stringify({
        message: this.newMessage,
        user_id: this.userStore.user.id // ID отправителя
      }));

      this.newMessage = ''; // Очистить поле ввода после отправки
    }
  }
};
</script>

