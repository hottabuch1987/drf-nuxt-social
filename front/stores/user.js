import { defineStore } from 'pinia';
import axios from 'axios';

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            isAuthenticated: false,
            id: null,
            username: null,
            email: null,
            access: null,
            refresh: null,
            avatar: null,
            first_name: null,
            last_name: null,
            bio: null,
            phone: null,
        },
    }),

    actions: {
        initStore() {
            if (process.client) { // Проверка на клиенте
                // console.log('initStore', localStorage.getItem('user.access'));

                if (localStorage.getItem('user.access')) {
                    console.log('User has access!');

                    this.user.access = localStorage.getItem('user.access');
                    this.user.refresh = localStorage.getItem('user.refresh');
                    this.user.id = localStorage.getItem('user.id');
                    this.user.username = localStorage.getItem('user.username');
                    this.user.email = localStorage.getItem('user.email');
                    this.user.first_name = localStorage.getItem('user.first_name');
                    this.user.last_name = localStorage.getItem('user.last_name');
                    this.user.bio = localStorage.getItem('user.bio');
                    this.user.phone = localStorage.getItem('user.phone');
                    this.user.avatar = localStorage.getItem('user.avatar');
                    this.user.isAuthenticated = true;
                 
                    // console.log('Initialized user:this.user.is_trainer ', this.user.is_trainer );

                    this.refreshToken();
                    // console.log('Initialized user:', this.user);

                 
                    // console.log('Liked postssss:', this.likedPosts);
                } 
            }
        },

        setToken(data) {
            if (process.client) { // Проверка на клиенте
                console.log('setToken', data);

                this.user.access = data.access;
                this.user.refresh = data.refresh;
                this.user.isAuthenticated = true;

                localStorage.setItem('user.access', data.access);
                localStorage.setItem('user.refresh', data.refresh);
            }
        },

        removeToken() {
            if (process.client) { // Проверка на клиенте
                console.log('removeToken');

                this.user = {
                    isAuthenticated: false,
                    id: null,
                    username: null,
                    email: null,
                    access: null,
                    refresh: null,
                    avatar: null,
                    first_name: null,
                    last_name: null,
                    bio: null,
                    phone: null,
                
                };

                localStorage.removeItem('user.access');
                localStorage.removeItem('user.refresh');
                localStorage.removeItem('user.id');
                localStorage.removeItem('user.username');
                localStorage.removeItem('user.email');
                localStorage.removeItem('user.first_name');
                localStorage.removeItem('user.last_name');
                localStorage.removeItem('user.bio');
                localStorage.removeItem('user.phone');
                localStorage.removeItem('user.avatar');
               
            }
        },

        setUserInfo(user) {
            if (process.client) { // Проверка на клиенте
                console.log('setUserInfo', user);

                if (user && user.id) {
                    this.user.id = user.id;
                }

                this.user.username = user.username;
                this.user.email = user.email;
                this.user.first_name = user.first_name;
                this.user.last_name = user.last_name;
                this.user.bio = user.bio;
                this.user.phone = user.phone;
                this.user.avatar = user.avatar;
        

                localStorage.setItem('user.id', this.user.id);
                localStorage.setItem('user.username', this.user.username);
                localStorage.setItem('user.email', this.user.email);
                localStorage.setItem('user.first_name', this.user.first_name);
                localStorage.setItem('user.last_name', this.user.last_name);
                localStorage.setItem('user.bio', this.user.bio);
                localStorage.setItem('user.phone', this.user.phone);
                localStorage.setItem('user.avatar', this.user.avatar);
         
            }
        },

        refreshToken() {
            axios.post('/refresh/', {
                refresh: this.user.refresh
            })
            .then((response) => {
                this.user.access = response.data.access;
                if (process.client) { // Проверка на клиенте
                    localStorage.setItem('user.access', response.data.access);
                }
                axios.defaults.headers.common["Authorization"] = "Bearer " + response.data.access;
            })
            .catch((error) => {
                console.log(error);
                this.removeToken();
            });
        },

        setAvatar(avatarUrl) {
            if (process.client) { // Проверка на клиенте
                this.user.avatar = avatarUrl;
                localStorage.setItem('user.avatar', avatarUrl);
            }
        },
        removeAvatar() {
                if (process.client) {
                    this.user.avatar = null; // Сброс аватара в состояние
                    localStorage.removeItem('user.avatar'); // Удаление из localStorage
            }
        }
    },
});