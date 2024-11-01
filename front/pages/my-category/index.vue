<template>
  <div>
    <div class="text-center p-10">
      <h1 class="text-4xl text-gray-400 font-semibold">Мои категории</h1>
      <button @click="showCreateForm = !showCreateForm" class="mt-4 p-2 bg-blue-400 text-white rounded hover:bg-blue-600 transition">
        {{ showCreateForm ? 'Отменить создание' : 'Создать категорию' }}
      </button>
     
    </div>

    <Spinner v-if="isLoading" />

    <section
      v-else
      class="w-fit mx-auto grid grid-cols-1 lg:grid-cols-3 md:grid-cols-2 justify-items-center justify-center gap-y-20 gap-x-14 mt-10 mb-5 text-gray-400"
    >
      <div v-if="!categories.length">Категорий нет</div>

      <!-- Создание категории -->
      <transition name="fade">

        <div v-if="showCreateForm" class="transition duration-500 ease-in-out transform bg-gray-100 rounded p-5 opacity-100 scale-100"

          enter-active-class="transition duration-500 ease-in-out"

          enter-from-class="opacity-0 scale-95"

          enter-to-class="opacity-100 scale-100"

          leave-active-class="transition duration-500 ease-in-out"

          leave-from-class="opacity-100 scale-100"

          leave-to-class="opacity-0 scale-95"

        >

          <h2 class="text-2xl font-bold">Создать категорию</h2>

          <form @submit.prevent="submitCategory" enctype="multipart/form-data">

            <div class="mb-4">

              <label class="block text-gray-400">Название</label>

              <input v-model="newCategory.name" type="text" required class="border border-gray-300 rounded p-2 w-full" />

            </div>

            <div class="mb-4">

              <label class="block text-gray-400" for="avatar">Изображение</label>

              <input type="file" @change="handleFileUpload" accept="image/*" class="border border-gray-300 rounded p-2 w-full" />

            </div>

            <div class="mb-4">

              <label class="inline-flex items-center">

                <input type="checkbox" v-model="newCategory.is_published" class="mr-2" />

                <span>Опубликовать</span>

              </label>

            </div>

            <button type="submit" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">Создать</button>

          </form>

        </div>

      </transition>
       <!-- Создание категории -->
       <!-- Вывод  категории -->
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="w-72 bg-white shadow-md rounded-xl duration-500 hover:scale-105 hover:shadow-xl"
      >
      
      <nuxt-link :to="`/my-category/${cat.slug}/`">
      <img :src="cat.get_image" alt="Category" class="h-80 w-72 object-cover rounded-t-xl" />
      
      <span class="text-gray-400 mr-3 uppercase text-xs">{{ cat.name }}</span>
      
      
      </nuxt-link>
        
        <!-- <img :src="cat.get_image" alt="Category" class="h-80 w-72 object-cover rounded-t-xl" />
        <span class="text-gray-400 mr-3 uppercase text-xs">{{ cat.name }}</span> -->
          <!-- Кнопка удаления -->
          <button @click="deleteCategory(cat)" class="text-red-600 hover:text-red-800">
            <svg  version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="18.294px" height="18.88px" viewBox="0 0 108.294 122.88" enable-background="new 0 0 108.294 122.88" xml:space="preserve">
              <g>
                  <path fill="red" d="M4.873,9.058h33.35V6.2V6.187c0-0.095,0.002-0.186,0.014-0.279c0.075-1.592,0.762-3.037,1.816-4.086l-0.007-0.007 c1.104-1.104,2.637-1.79,4.325-1.806l0.023,0.002V0h0.031h19.884h0.016c0.106,0,0.207,0.009,0.309,0.022 c1.583,0.084,3.019,0.76,4.064,1.81c1.102,1.104,1.786,2.635,1.803,4.315l-0.003,0.021h0.014V6.2v2.857h32.909h0.017 c0.138,0,0.268,0.014,0.401,0.034c1.182,0.106,2.254,0.625,3.034,1.41l0.004,0.007l0.005-0.007 c0.851,0.857,1.386,2.048,1.401,3.368l-0.002,0.032h0.014v0.032v10.829c0,1.472-1.195,2.665-2.667,2.665h-0.07H2.667 C1.195,27.426,0,26.233,0,24.762v-0.063V13.933v-0.014c0-0.106,0.004-0.211,0.018-0.315v-0.021 c0.089-1.207,0.624-2.304,1.422-3.098l-0.007-0.002C2.295,9.622,3.49,9.087,4.81,9.069l0.032,0.002V9.058H4.873L4.873,9.058z M77.79,49.097h-5.945v56.093h5.945V49.097L77.79,49.097z M58.46,49.097h-5.948v56.093h5.948V49.097L58.46,49.097z M39.13,49.097 h-5.946v56.093h5.946V49.097L39.13,49.097z M10.837,31.569h87.385l0.279,0.018l0.127,0.007l0.134,0.011h0.009l0.163,0.023 c1.363,0.163,2.638,0.789,3.572,1.708c1.04,1.025,1.705,2.415,1.705,3.964c0,0.098-0.009,0.193-0.019,0.286l-0.002,0.068 l-0.014,0.154l-7.393,79.335l-0.007,0.043h0.007l-0.016,0.139l-0.051,0.283l-0.002,0.005l-0.002,0.018 c-0.055,0.331-0.12,0.646-0.209,0.928l-0.007,0.022l-0.002,0.005l-0.009,0.018l-0.023,0.062l-0.004,0.021 c-0.118,0.354-0.264,0.698-0.432,1.009c-1.009,1.88-2.879,3.187-5.204,3.187H18.13l-0.247-0.014v0.003l-0.011-0.003l-0.032-0.004 c-0.46-0.023-0.889-0.091-1.288-0.202c-0.415-0.116-0.818-0.286-1.197-0.495l-0.009-0.002l-0.002,0.002 c-1.785-0.977-2.975-2.882-3.17-5.022L4.88,37.79l-0.011-0.125l-0.011-0.247l-0.004-0.116H4.849c0-1.553,0.664-2.946,1.707-3.971 c0.976-0.955,2.32-1.599,3.756-1.726l0.122-0.004v-0.007l0.3-0.013l0.104,0.002V31.569L10.837,31.569z M98.223,36.903H10.837 v-0.007l-0.116,0.004c-0.163,0.022-0.322,0.106-0.438,0.222c-0.063,0.063-0.104,0.132-0.104,0.179h-0.007l0.007,0.118l7.282,79.244 h-0.002l0.002,0.012c0.032,0.376,0.202,0.691,0.447,0.825l-0.002,0.004l0.084,0.032l0.063,0.012h0.077h72.695 c0.207,0,0.399-0.157,0.518-0.377l0.084-0.197l0.054-0.216l0.014-0.138h0.005l7.384-79.21L98.881,37.3 c0-0.045-0.041-0.111-0.103-0.172c-0.12-0.118-0.286-0.202-0.451-0.227L98.223,36.903L98.223,36.903z M98.334,36.901h-0.016H98.334 L98.334,36.901z M98.883,37.413v-0.004V37.413L98.883,37.413z M104.18,37.79l-0.002,0.018L104.18,37.79L104.18,37.79z M40.887,14.389H5.332v7.706h97.63v-7.706H67.907h-0.063c-1.472,0-2.664-1.192-2.664-2.664V6.2V6.168h0.007 c-0.007-0.22-0.106-0.433-0.259-0.585c-0.137-0.141-0.324-0.229-0.521-0.252h-0.082h-0.016H44.425h-0.031V5.325 c-0.213,0.007-0.422,0.104-0.576,0.259l-0.004-0.004l-0.007,0.004c-0.131,0.134-0.231,0.313-0.259,0.501l0.007,0.102V6.2v5.524 C43.554,13.196,42.359,14.389,40.887,14.389L40.887,14.389z"/>
              </g>
          </svg>
          </button> 
          <!-- Кнопка удаления -->

        
        <a href="#" v-if="cat.products.length">

          <div class="px-4 py-3 w-72">
            
            <p class="text-lg font-bold text-black truncate block capitalize"></p>
            <div class="flex items-center" v-for="product in cat.products" :key="product.id">
              <p class="text-lg font-semibold text-black cursor-auto my-3">
                <nuxt-link :to="`/my-product/${product.slug}/`" class="font-bold text-red-600">{{ product.name }}</nuxt-link>
              </p>
              
              <div class="ml-auto">
                <nuxt-link :to="`/my-product/${product.slug}/`">
               
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="20"
                    height="20"
                    fill="currentColor"
                    class="bi bi-bag-plus"
                    viewBox="0 0 16 16"
                  >
                    <path fill-rule="evenodd" d="M8 7.5a.5.5 0 0 1 .5.5v1.5H10a.5.5 0 0 1 0 1H8.5V12a.5.5 0 0 1-1 0v-1.5H6a.5.5 0 0 1 0-1h1.5V8a.5.5 0 0 1 .5-.5z" />
                    <path d="M8 1a2.5 2.5 0 0 1 2.5 2.5V4h-5v-.5A2.5 2.5 0 0 1 8 1zm3.5 3v-.5a3.5 3.5 0 1 0-7 0V4H1v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V4h-3.5zM2 5h12v9a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5z" />
                  </svg>
                </nuxt-link>
               
              </div>
            </div>
            

            
          </div>
        </a>
        <span v-else> Нет программ  </span>
              

      </div>
    </section>
  </div>
</template>

<script>
import axios from 'axios';
import Spinner from '@/components/Spinner.vue';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  
  components: {
    Spinner,
    
  },
  data() {
    return {
      categories: [],
      isLoading: true,
      showCreateForm: false,
      showCreateFormProduct: false,
      newCategory: {
        name: '',
        // slug: '',
        products: [],
        owner: '',
        is_published: true,
        image: '', // Для хранения загружаемого изображения
      },
      toastStore: useToastStore(),
    };
  },
  mounted() {
    this.getCategories();
    this.setOwner();
    document.title = "Мои Обьявления | Offer";
  },
  methods: {
    getCategories() {
      this.isLoading = true;
      axios
        .get('/my-category/')
        .then(response => {
          this.categories = response.data;
          console.log(response.data, 'response.data');
        })
        .catch(error => {
          console.log('Ошибка при загрузке категорий:', error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    setOwner() {
      const userStore = useUserStore();
      if (userStore.user && userStore.user.id) {
        this.newCategory.owner = userStore.user.id;
      } else {
        console.error('Пользователь не найден или не имеет ID');
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      console.log(file);
      if (file) {
        this.newCategory.image = file; // Сохраняем загруженное изображение
        console.log(this.newCategory.image, 'this.newCategory.image');
      }
    },
    deleteCategory(category) {
      if (confirm(`Вы уверены, что хотите удалить категорию? Все программы связанные с категорий  "${category.name}" будут удалены!`)) {
        this.isLoading = true;
          axios
            .delete(`/my-category/${category.slug}/`) // удаление происходит по slug
            .then(() => {
              this.categories = this.categories.filter(cat => cat.id !== category.id); // Обновляем список категорий
              this.toastStore.showToast(5000, `Категория ${category.name} удалена!`, 'bg-emerald-500');
            })
            .catch(error => {
              console.error('Ошибка при удалении категории:', error);
              this.toastStore.showToast(5000, 'Ошибка при удалении категории!', 'bg-red-500'); 
            })
            .finally(() => {
              this.isLoading = false;
            });
        }
      },
    submitCategory() {
      this.isLoading = true;
      const formData = new FormData(); // Создаем новый объект FormData

      // Добавляем поля к FormData
      formData.append('name', this.newCategory.name);
      // formData.append('slug', this.newCategory.slug);
      formData.append('is_published', this.newCategory.is_published);
      formData.append('owner', this.newCategory.owner);
      if (this.newCategory.image) {
        formData.append('image', this.newCategory.image); // Добавляем изображение
      }
      console.log(formData, 'formData');

      axios
        .post('/my-category/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Указываем тип контента
          },
        })
        .then(response => {
          this.categories.push(response.data);
          // Сбрасываем поля
          this.newCategory = {
            name: '',
            // slug: '',
            products: [],
            owner: this.newCategory.owner || '',
            is_published: true,
            image: '',
          };
          this.showCreateForm = false;
          this.toastStore.showToast(5000, `Категория ${response.data.name} создана!`, 'bg-emerald-500');
         
        })
        .catch(error => {
          console.error('Ошибка при создании категории:', error);
          this.toastStore.showToast(5000, 'Ошибка при создании категории!', 'bg-red-500');
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
  },
};
</script>

