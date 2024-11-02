
<template>
  <div class="max-w-2xl mx-auto p-10 bg-white rounded-lg shadow-md">
    <div class="text-center mb-6">
      <h1 class="font-bold text-4xl text-gray-400 mb-4">
        {{ isEditing ? "Редактировать пост" : product.name }}
      </h1>
      <div v-if="!product" class="text-gray-400 text-lg">Нет постов в этой категории.</div>
    </div>

    <Spinner v-if="isLoading" />

    <div v-else>
      <div class="relative rounded-md overflow-hidden shadow-md hover:shadow-lg" v-if="product">
        <img class="w-full object-cover h-64" :src="product.get_image" alt="Product Image" v-if="product.get_image" />
        <div v-if="product.get_image" class="absolute top-0 right-0 bg-red-500 text-white px-2 py-1 m-2 rounded-md text-sm font-medium">
         {{ product.is_published ? 'Опубликован' : 'Не опубликован' }}
        </div>

        <div class="mt-4" v-if="product.get_video">
          <h4 class="font-medium text-lg">Видео инструкция</h4>
          <video  class="w-full mt-2" controls>
            <source :src="product.get_video" type="video/mp4">
          </video>
        </div>
     

        <div class="p-4">
          <h3 class="text-lg font-bold text-gray-500 mb-2">{{ product.name }}</h3>
          <p class="text-gray-600 text-sm mb-4"></p>{{ product.description }}
        </div>
      </div>

      <section v-if="isEditing" class="mt-10 text-gray-400">
        <form @submit.prevent="submitEdit">
          <div class="mb-4">
            <label class="block text-gray-400 font-semibold">Название</label>
            <input
              v-model="editProduct.name"
              type="text"
              required
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="block text-gray-400 font-semibold">Описание</label>
            <input
              v-model="editProduct.description"
              type="text"
              required
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>


          <div class="mb-4">
            <label class="block  font-semibold" for="avatar"></label>
            <div v-if="editProduct.imageURL">
              <img :src="editProduct.imageURL" alt="Текущее изображение" class="rounded-lg mb-4" />
            </div>
            <input
              type="file"
              @change="handleFileUpload"
              accept="image/*"
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="block  font-semibold">Видео</label>
            <input
              type="file"
              @change="handleVideoUpload"
              accept="video/*"
              class="border border-gray-300 rounded p-2 w-full"
            />
          </div>

          <div class="mb-4">
            <label class="inline-flex items-center">
              <input
                type="checkbox"
                v-model="editProduct.is_published"
                class="mr-2"
              />
              <span>Опубликовать</span>
            </label>
          </div>

          <div class="flex justify-between mt-4">
            <button type="submit" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">
              Сохранить изменения
            </button>
            <button
              @click.prevent="isEditing = false"
              class="bg-gray-500 text-white p-2 rounded hover:bg-gray-600 transition"
            >
              Отменить
            </button>
          </div>
        </form>
      </section>

      <!-- Кнопки "Удалить продукт" и "Редактировать продукт" вынесены сюда, чтобы они отображались постоянно -->
      <div class="flex justify-between mt-4">
        <button @click="deleteProduct(product)" class="text-red-600 hover:text-red-800">
          <svg  version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="18.294px" height="18.88px" viewBox="0 0 108.294 122.88" enable-background="new 0 0 108.294 122.88" xml:space="preserve">
              <g>
                  <path fill="red" d="M4.873,9.058h33.35V6.2V6.187c0-0.095,0.002-0.186,0.014-0.279c0.075-1.592,0.762-3.037,1.816-4.086l-0.007-0.007 c1.104-1.104,2.637-1.79,4.325-1.806l0.023,0.002V0h0.031h19.884h0.016c0.106,0,0.207,0.009,0.309,0.022 c1.583,0.084,3.019,0.76,4.064,1.81c1.102,1.104,1.786,2.635,1.803,4.315l-0.003,0.021h0.014V6.2v2.857h32.909h0.017 c0.138,0,0.268,0.014,0.401,0.034c1.182,0.106,2.254,0.625,3.034,1.41l0.004,0.007l0.005-0.007 c0.851,0.857,1.386,2.048,1.401,3.368l-0.002,0.032h0.014v0.032v10.829c0,1.472-1.195,2.665-2.667,2.665h-0.07H2.667 C1.195,27.426,0,26.233,0,24.762v-0.063V13.933v-0.014c0-0.106,0.004-0.211,0.018-0.315v-0.021 c0.089-1.207,0.624-2.304,1.422-3.098l-0.007-0.002C2.295,9.622,3.49,9.087,4.81,9.069l0.032,0.002V9.058H4.873L4.873,9.058z M77.79,49.097h-5.945v56.093h5.945V49.097L77.79,49.097z M58.46,49.097h-5.948v56.093h5.948V49.097L58.46,49.097z M39.13,49.097 h-5.946v56.093h5.946V49.097L39.13,49.097z M10.837,31.569h87.385l0.279,0.018l0.127,0.007l0.134,0.011h0.009l0.163,0.023 c1.363,0.163,2.638,0.789,3.572,1.708c1.04,1.025,1.705,2.415,1.705,3.964c0,0.098-0.009,0.193-0.019,0.286l-0.002,0.068 l-0.014,0.154l-7.393,79.335l-0.007,0.043h0.007l-0.016,0.139l-0.051,0.283l-0.002,0.005l-0.002,0.018 c-0.055,0.331-0.12,0.646-0.209,0.928l-0.007,0.022l-0.002,0.005l-0.009,0.018l-0.023,0.062l-0.004,0.021 c-0.118,0.354-0.264,0.698-0.432,1.009c-1.009,1.88-2.879,3.187-5.204,3.187H18.13l-0.247-0.014v0.003l-0.011-0.003l-0.032-0.004 c-0.46-0.023-0.889-0.091-1.288-0.202c-0.415-0.116-0.818-0.286-1.197-0.495l-0.009-0.002l-0.002,0.002 c-1.785-0.977-2.975-2.882-3.17-5.022L4.88,37.79l-0.011-0.125l-0.011-0.247l-0.004-0.116H4.849c0-1.553,0.664-2.946,1.707-3.971 c0.976-0.955,2.32-1.599,3.756-1.726l0.122-0.004v-0.007l0.3-0.013l0.104,0.002V31.569L10.837,31.569z M98.223,36.903H10.837 v-0.007l-0.116,0.004c-0.163,0.022-0.322,0.106-0.438,0.222c-0.063,0.063-0.104,0.132-0.104,0.179h-0.007l0.007,0.118l7.282,79.244 h-0.002l0.002,0.012c0.032,0.376,0.202,0.691,0.447,0.825l-0.002,0.004l0.084,0.032l0.063,0.012h0.077h72.695 c0.207,0,0.399-0.157,0.518-0.377l0.084-0.197l0.054-0.216l0.014-0.138h0.005l7.384-79.21L98.881,37.3 c0-0.045-0.041-0.111-0.103-0.172c-0.12-0.118-0.286-0.202-0.451-0.227L98.223,36.903L98.223,36.903z M98.334,36.901h-0.016H98.334 L98.334,36.901z M98.883,37.413v-0.004V37.413L98.883,37.413z M104.18,37.79l-0.002,0.018L104.18,37.79L104.18,37.79z M40.887,14.389H5.332v7.706h97.63v-7.706H67.907h-0.063c-1.472,0-2.664-1.192-2.664-2.664V6.2V6.168h0.007 c-0.007-0.22-0.106-0.433-0.259-0.585c-0.137-0.141-0.324-0.229-0.521-0.252h-0.082h-0.016H44.425h-0.031V5.325 c-0.213,0.007-0.422,0.104-0.576,0.259l-0.004-0.004l-0.007,0.004c-0.131,0.134-0.231,0.313-0.259,0.501l0.007,0.102V6.2v5.524 C43.554,13.196,42.359,14.389,40.887,14.389L40.887,14.389z"/>
              </g>
          </svg>
          
        </button>
        <button @click="isEditing = true" class="bg-green-500 text-white p-2 rounded hover:bg-green-600 transition">Редактировать пост</button>
      </div>
    </div>
  </div>
</template>



  
<script>
  import axios from "axios";
  import Spinner from "@/components/Spinner.vue";
  import { useToastStore } from '@/stores/toast';
  
  export default {
    components: {
      Spinner,
    },
    data() {
      return {
        product: {},
        editProduct: {
          name: '',
          video: null,
          description: '',
          // slug: '',
          is_published: false,
          image: null, // Для хранения загруженного изображения
          imageURL: "", // Для безопасного отображения URL изображения
        },
        isLoading: true,
        isEditing: false,
        toastStore: useToastStore(),
      };
    },
    async mounted() {
      const slug = this.$route.params.slug; // Получаем slug из параметров маршрута
      await this.getProduct(slug);
      
      
    },
    methods: {
      async getProduct(slug) {
        this.isLoading = true;
        try {
          const response = await axios.get(`/my-product/${slug}/`);
          this.product = response.data;
          
          this.editProduct = {
            name: this.product.name,
            video: this.product.video,
            description: this.product.description,
            is_published: this.product.is_published,
            imageURL: this.product.get_image || "", // Сохраняем URL существующего изображения
          };
        } catch (error) {
          console.error("Ошибка при загрузке поста:", error);
        } finally {
          this.isLoading = false;
        }
      },
      handleFileUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.editProduct.image = file; // Сохраняем загруженное изображение
          // Создаем объект URL для отображения
          this.editProduct.imageURL = URL.createObjectURL(file);
        } else {
        // Если файл не выбран, оставляем текущее изображение
        // this.editCategory.imageURL сохранится как есть
        }
      },
      handleVideoUpload(event) {
        const file = event.target.files[0];
        if (file) {
          this.editProduct.video = file; // Сохраняем загруженное видео
        } else {
        // Если файл не выбран, оставляем текущее видео
        console.log('Файл не выбран');
        }
      },
      
      deleteProduct(product) {
          if (confirm(`Вы уверены, что хотите удалить пост "${product.name}"?`)) {
              this.isLoading = true;
              axios
                  .delete(`/my-product/${product.slug}/`)
                  .then(() => {
                      // Если вы действительно имеете дело с одним продуктом, просто обнуляем его
                      this.product = null; // Продукт успешно удалён
                      this.toastStore.showToast(5000, 'Пост успешно удален!', 'bg-green-500');
                      this.$router.push({ name: 'my-product' });
                      
                      // Вы можете перенаправить пользователя или выполнить другие действия здесь
                  })
                  .catch(error => {
                      console.error('Ошибка при удалении Поста:', error);
                      this.toastStore.showToast(5000, 'Ошибка при удалении Поста!', 'bg-red-500'); 
                  })
                  .finally(() => {
                      this.isLoading = false;
                  });
          }
      },


      async submitEdit() {
        this.isLoading = true;
        const formData = new FormData();
        formData.append("name", this.editProduct.name);
        // formData.append("slug", this.editProduct.slug);
        formData.append("is_published", this.editProduct.is_published);
        formData.append("description", this.editProduct.description);
  
        // Проверяем, есть ли изображение или видео, перед добавлением в FormData
        if (this.editProduct.image) {
          formData.append("image", this.editProduct.image);
        }
        if (this.editProduct.video) {

          formData.append("video", this.editProduct.video);

        }
  
        try {
          const response = await axios.put(
            `/my-product/${this.product.slug}/`,
            formData,
            {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            }
          );
          this.product = response.data; // Обновляем продукт
          this.isEditing = false; // Закрываем форму редактирования
          this.toastStore.showToast(5000, 'Пост успешно обновлен!', 'bg-green-500');
          
        } catch (error) {
          console.error("Ошибка при обновлении Поста:", error);
          this.toastStore.showToast(5000, 'Ошибка при изменении Поста!', 'bg-red-500');
          
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
</script>
  
  

  