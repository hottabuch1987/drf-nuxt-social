
    <template>
      
      <div v-if="userStore.user.isAuthenticated">
        <div class="text-center p-10">
          <h1 class=" text-gray-400 text-3xl font-bold" v-if="users.length">Все Пользователи</h1>
          <h1 class=" text-gray-400 text-3xl font-bold" v-else>Нет Пользователей</h1>
        </div>
    
        <Spinner v-if="isLoading" />
    
        <section
          v-else
          class="w-fit mx-auto grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 justify-items-center justify-center gap-y-20 gap-x-14 mt-10 mb-5"
        >
          <div
            id="Projects"
            v-for="user in users" 
            :key="user.id"
            class="w-72 bg-white shadow-md rounded-xl duration-500 hover:scale-105 hover:shadow-xl"
          >
          <nuxt-link :to="`/profile/${user.slug}`">
            <span class="text-gray-400 mr-3 uppercase text-xs">{{ user.username }}</span>

            <div>
              <img v-if="user.photos.length > 0 && user.photos[user.photos.length - 1].get_image" 
                  :src="user.photos[user.photos.length - 1].get_image" 
                  alt="Users" 
                  class="h-80 w-72 object-cover rounded-t-xl" />
              <img v-else src="https://cdn-icons-png.flaticon.com/512/149/149071.png" 
                  alt="Avatar User" 
                  class="h-80 w-72 rounded-full border-4 border-white dark:border-gray-800 mx-auto my-4" />
            </div>

            <div class="px-4 py-3 w-72">
              <span class="text-gray-400 mr-3 uppercase text-xs" v-if="user.birth_date">{{formatDate(user.birth_date)}} {{ user.gender }} </span>
              <p class="text-lg font-bold text-black truncate block capitalize"></p>
              <div class="flex items-center">
                <p class="text-sm font-semibold text-black cursor-auto my-3">
                  <nuxt-link :to="`/profile/${user.slug}`" class="font-bold text-red-600">{{user.last_name}} {{ user.first_name }}</nuxt-link>
                </p>
              </div>
            </div>
          </nuxt-link>

          </div>
        </section>
      </div>
    
      <div v-else class="flex flex-col items-center">
        <h1 class="text-center text-4xl text-gray-400">Войдите или создайте аккаунт</h1>
        
        <div class="flex flex-col items-center mt-4 gap-2">
          <nuxt-link
            to="/signup"
            class="text-2xl rounded-md to-emerald-400 px-3 py-1.5  text-bold font-medium shadow-md text-gray-400 transition-transform duration-200 ease-in-out hover:scale-[1.03]"
          >
            Регистрация
          </nuxt-link>
    
          <nuxt-link 
            :to="{'name': 'login'}" 
            class="text-2xl rounded-md to-emerald-400 px-3 py-1.5  text-bold font-medium shadow-md text-gray-400 transition-transform duration-200 ease-in-out hover:scale-[1.03]"
          >
            Войти
          </nuxt-link>
    
          
        </div>
      </div>
      <!--  -->

    
  <!--  -->
</template>

<script>
import axios from 'axios'
import { DateTime } from "luxon";
import { useUserStore } from '@/stores/user';

export default {

  data() {
    return {
      users: [],
      isLoading: true,
      userStore: useUserStore(),
    }
  },
   mounted() {

    this.getUsers();

    document.title = "Пользователи | Poster";

  },
  methods: {
    getUsers() {
      this.isLoading = true; 
      axios
        .get('/users/')
        .then(response => {
          this.users = response.data; 
          console.log(response.data)
        })
        .catch(error => {
          console.log('error', error)
        })
        .finally(() => {
          this.isLoading = false; // Устанавливаем isLoading в false после получения данных
        });
    },
    formatDate(date) {
      return DateTime.fromISO(date).toLocaleString(DateTime.DATE_MED);
    },
  }
}
</script>
