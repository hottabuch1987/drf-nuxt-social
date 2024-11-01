<template>
    <div>
      <div class="shadow-orange-300" v-for="(msg, index) in messages" :key="index">{{ msg }}</div>
      <input v-model="message" @keyup.enter="sendMessage" />
    </div>
  </template>
  
  <script>

  
  export default {
    props: {
      userId: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        messages: [],
        message: '',
        socket: null,
      };
    },
    mounted() {
      this.socket = new WebSocket(`ws://127.0.0.1:8000/ws/${this.userId}/`);
  
      this.socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        // Предполагается, что вы получаете объект с полем message
        this.messages.push(data.message);
      };
    },
    methods: {
      sendMessage() {
        if (this.message.trim()) { // Проверка на пустое сообщение
          this.socket.send(JSON.stringify({ message: this.message }));
          this.message = '';
        }
      },
    },
  };
  </script>
  
  