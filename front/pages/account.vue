<template>
<div tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-00 rounded-box w-100">      
  <div class="rounded-lg bg-base-300 p-3 drop-shadow-xl divide-y divide-neutral">   

    <ProfileCard :user="userStore.user" />
    <div v-for="(status, username) in onlineStatus" :key="username" class="status-message space-x-3 py-3 px-4">
            <span v-if="status === 'online'" class="text-green-500">Online</span>
            <span v-else class="text-red-500">Offline</span>
    </div>
     <div aria-label="navigation" class="py-2">
        <nuxt-link :to="{'name': 'direct'}" class="flex items-center leading-6 space-x-3 py-3 px-4 w-full text-lg text-gray-600 focus:outline-none hover:bg-gray-100 rounded-md transition-transform duration-200 ease-in-out hover:scale-[1.01]">
            <svg class="w-7 h-7" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none">
                            <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                            <path d="M9 12l2 2l4 -4"></path>
            </svg>
            <span>Мои сообщения</span>
        </nuxt-link>
        <MyProgramm />
        
        <EditAccountLink />
        <ChangePasswordLink />
        <LogoutButton @logout="logout"/>

    
      </div>
    </div>
</div>

</template>

<script>
import axios from 'axios';
import { DateTime } from 'luxon';
import { ref, onMounted } from 'vue'; 
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
    name: 'account',
    setup() {
        const userStore = useUserStore();
        const toastStore = useToastStore();
        const router = useRouter();
        const onlineStatus = ref({});
        let socket;

        const connectWebSocket = () => {
        socket = new WebSocket(`ws://localhost:8000/ws/user-status/`);

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            onlineStatus.value[data.username] = data.status; // Обновляем статус пользователя
        };

        socket.onclose = () => {
            console.log('WebSocket connection closed');
            };
        };
        onMounted(() => {
            connectWebSocket();
        });

        onBeforeUnmount(() => {
            if (socket) {
                socket.close();
            }
        });

        const logout = () => {
            userStore.removeToken();
            toastStore.showToast(5000, 'Вы вышли из системы успешно', 'bg-green-500');
            router.push({ name: 'login' });
        };

        

        const formatDate = (dateString) => {
            return DateTime.fromISO(dateString).toLocaleString(DateTime.DATETIME_MED);
        };
        


        return {
            userStore,
            formatDate,
            logout,
            onlineStatus,
        };
    },

    mounted() {
        document.title = "Мой профиль | Poster";
    },
}
</script>
