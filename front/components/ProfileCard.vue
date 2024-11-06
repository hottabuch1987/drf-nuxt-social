<template>
  <div class="flex flex-col space-y-4 p-4">
    <div class="flex space-x-4 items-center">
      <img v-if="photos.length === 0" src="@/assets/img/default.png" class="w-36 h-36 shrink-0 rounded-full" alt="Default Avatar" />
      
      <div class="overflow-hidden flex-1">
        <div class="flex transition-transform duration-500" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
          <div v-for="(photo, index) in photos" :key="photo.id" class="min-w-full flex h-full">
            <img v-if="photo.get_image"
                 :src="photo.get_image"
                 class="w-[200px] h-[200px] rounded-full shrink-0 opacity-80 hover:opacity-100"
                 alt="Фото"
                 @click="openModal(index)" />
          </div>
        </div>
      </div>
    </div>

    <!-- Контейнер для добавления фото и кнопок навигации -->
    <div class="flex items-center justify-between mt-4 max-w-[300px]">
      <form @submit.prevent.default enctype="multipart/form-data"> 
        <input type="file" @change="handleFileChange" required ref="fileInput" style="display: none;" />
        <div @click="selectFile" class="cursor-pointer hover:bg-gray-200 p-2 rounded-full">
          <svg xmlns="http://www.w3.org/2000/svg" shape-rendering="geometricPrecision" text-rendering="geometricPrecision" image-rendering="optimizeQuality" fill-rule="evenodd" clip-rule="evenodd" viewBox="0 0 512 511.99" width="28" height="28">
              <path fill="#00AB42" fill-rule="nonzero" d="M256 0c70.68 0 134.69 28.66 181.01 74.98C483.35 121.31 512 185.31 512 255.99c0 70.68-28.66 134.69-74.99 181.02-46.32 46.32-110.33 74.98-181.01 74.98-70.68 0-134.69-28.66-181.02-74.98C28.66 390.68 0 326.67 0 255.99S28.65 121.31 74.99 74.98C121.31 28.66 185.32 0 256 0zm116.73 236.15v39.69c0 9.39-7.72 17.12-17.11 17.12h-62.66v62.66c0 9.4-7.71 17.11-17.11 17.11h-39.7c-9.4 0-17.11-7.69-17.11-17.11v-62.66h-62.66c-9.39 0-17.11-7.7-17.11-17.12v-39.69c0-9.41 7.69-17.11 17.11-17.11h62.66v-62.67c0-9.41 7.7-17.11 17.11-17.11h39.7c9.41 0 17.11 7.71 17.11 17.11v62.67h62.66c9.42 0 17.11 7.76 17.11 17.11zm37.32-134.21c-39.41-39.41-93.89-63.8-154.05-63.8-60.16 0-114.64 24.39-154.05 63.8-39.42 39.42-63.81 93.89-63.81 154.05 0 60.16 24.39 114.64 63.8 154.06 39.42 39.41 93.9 63.8 154.06 63.8s114.64-24.39 154.05-63.8c39.42-39.42 63.81-93.9 63.81-154.06s-24.39-114.63-63.81-154.05z"/>
          </svg>
        </div>

        <div v-if="selectedFile" class="mt-2 text-gray-700">
          Выбран файл: {{ selectedFile.name }}
        </div>

        <button 
          v-if="selectedFile" 
          @click="submitPhoto"  
          class="bg-gray-200 text-gray-700 font-semibold my-2 p-2 rounded hover:bg-gray-300 transition"
        >
          Загрузить
        </button>
      </form>

  

      <button v-if="photos.length > 1" @click="nextSlide" class="w-[40px] h-[40px] bg-gray-300 text-white rounded-full shrink-0 opacity-70 hover:opacity-100">
        →
      </button>
    </div>

    <!-- Модальное окно для просмотра фотографий -->
    <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-70" @click.self="closeModal">
      <div class="bg-white p-5 rounded shadow-lg relative">
        <img :src="photos[currentPhotoIndex]?.get_image" class="max-w-full max-h-[80vh] rounded" alt="Фото" />
        <button @click="closeModal" class="mt-4 bg-gray-200 text-gray-700 p-2 rounded hover:bg-gray-300">Закрыть</button>
        <button @click="deletePhoto(photos[currentPhotoIndex].id)" class="absolute bottom-2 right-2 text-red-600 hover:text-red-800">
            <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="18.294px" height="18.88px" viewBox="0 0 108.294 122.88" enable-background="new 0 0 108.294 122.88" xml:space="preserve">
              <g>
                <path fill="currentColor" d="M4.873,9.058h33.35V6.2V6.187c0-0.095,0.002-0.186,0.014-0.279c0.075-1.592,0.762-3.037,1.816-4.086l-0.007-0.007 c1.104-1.104,2.637-1.79,4.325-1.806l0.023,0.002V0h0.031h19.884h0.016c0.106,0,0.207,0.009,0.309,0.022 c1.583,0.084,3.019,0.76,4.064,1.81c1.102,1.104,1.786,2.635,1.803,4.315l-0.003,0.021h0.014V6.2v2.857h32.909h0.017 c0.138,0,0.268,0.014,0.401,0.034c1.182,0.106,2.254,0.625,3.034,1.41l0.004,0.007l0.005-0.007 c0.851,0.857,1.386,2.048,1.401,3.368l-0.002,0.032h0.014v0.032v10.829c0,1.472-1.195,2.665-2.667,2.665h-0.07H2.667 C1.195,27.426,0,26.233,0,24.762v-0.063V13.933v-0.014c0-0.106,0.004-0.211,0.018-0.315v-0.021 c0.089-1.207,0.624-2.304,1.422-3.098l-0.007-0.002C2.295,9.622,3.49,9.087,4.81,9.069l0.032,0.002V9.058H4.873L4.873,9.058z M77.79,49.097h-5.945v56.093h5.945V49.097L77.79,49.097z M58.46,49.097h-5.948v56.093h5.948V49.097L58.46,49.097z M39.13,49.097 h-5.946v56.093h5.946V49.097L39.13,49.097z M10.837,31.569h87.385l0.279,0.018l0.127,0.007l0.134,0.011h0.009l0.163,0.023 c1.363,0.163,2.638,0.789,3.572,1.708c1.04,1.025,1.705,2.415,1.705,3.964c0,0.098-0.009,0.193-0.019,0.286l-0.002,0.068 l-0.014,0.154l-7.393,79.335l-0.007,0.043h0.007l-0.016,0.139l-0.051,0.283l-0.002,0.005l-0.002,0.018 c-0.055,0.331-0.12,0.646-0.209,0.928l-0.007,0.022l-0.002,0.005l-0.009,0.018l-0.023,0.062l-0.004,0.021 c-0.118,0.354-0.264,0.698-0.432,1.009c-1.009,1.88-2.879,3.187-5.204,3.187H18.13l-0.247-0.014v0.003l-0.011-0.003l-0.032-0.004 c-0.46-0.023-0.889-0.091-1.288-0.202c-0.415-0.116-0.818-0.286-1.197-0.495l-0.009-0.002l-0.002,0.002 c-1.785-0.977-2.975-2.882-3.17-5.022L4.88,37.79l-0.011-0.125l-0.011-0.247l-0.004-0.116H4.849c0-1.553,0.664-2.946,1.707-3.971 c0.976-0.955,2.32-1.599,3.756-1.726l0.122-0.004v-0.007l0.3-0.013l0.104,0.002V31.569L10.837,31.569z M98.223,36.903H10.837 v-0.007l-0.116,0.004c-0.163,0.022-0.322,0.106-0.438,0.222c-0.063,0.063-0.104,0.132-0.104,0.179h-0.007l0.007,0.118l7.282,79.244 h-0.002l0.002,0.012c0.032,0.376,0.202,0.691,0.447,0.825l-0.002,0.004l0.084,0.032l0.063,0.012h0.077h72.695 c0.207,0,0.399-0.157,0.518-0.377l0.084-0.197l0.054-0.216l0.014-0.138h0.005l7.384-79.21L98.881,37.3 c0-0.045-0.041-0.111-0.103-0.172c-0.12-0.118-0.286-0.202-0.451-0.227L98.223,36.903L98.223,36.903z M98.334,36.901h-0.016H98.334 L98.334,36.901z M98.883,37.413v-0.004V37.413L98.883,37.413z M104.18,37.79l-0.002,0.018L104.18,37.79L104.18,37.79z M40.887,14.389H5.332v7.706h97.63v-7.706H67.907h-0.063c-1.472,0-2.664-1.192-2.664-2.664V6.2V6.168h0.007 c-0.007-0.22-0.106-0.433-0.259-0.585c-0.137-0.141-0.324-0.229-0.521-0.252h-0.082h-0.016H44.425h-0.031V5.325 c-0.213,0.007-0.422,0.104-0.576,0.259l-0.004-0.004l-0.007,0.004c-0.131,0.134-0.231,0.313-0.259,0.501l0.007,0.102V6.2v5.524 C43.554,13.196,42.359,14.389,40.887,14.389L40.887,14.389z"/>
              </g>
            </svg>
        </button>
      </div>
    </div>


    <div class="space-y-2 flex flex-col flex-1 truncate text-gray-500">
        <strong class="truncate">{{ user.username }}</strong>
        <p class="font-normal text-base leading-tight truncate">{{ user.first_name }} {{ user.last_name }}</p>
        <strong class="font-normal text-base leading-tight truncate">{{ user.email }}</strong>
        <p class="font-normal text-base leading-tight truncate">{{ user.bio }}</p>
        <div class="inline-flex items-center space-x-2" v-if="user.active">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6 text-yellow-500">
            <path d="M12 .587l3.668 7.568 8.332 1.144-6.004 5.547 1.412 8.208L12 18.896l-7.408 3.883 1.412-8.208-6.004-5.547 8.332-1.144L12 .587z"/>
          </svg>
          <span> Бизнес аккаунт </span>
        </div>
      </div>
  </div>
</template>


<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { useToastStore } from '@/stores/toast';

export default {
  name: 'ProfileCard',
  props: {
    user: Object,
  },

  setup(props) {
    const fileInput = ref(null);
    const photos = ref([]);
    const userStore = useUserStore();
    const toastStore = useToastStore();
    const selectedFile = ref(null);
    const currentIndex = ref(0);
    const isModalOpen = ref(false);
    const currentPhotoIndex = ref(0);

    const handleFileChange = (event) => {
      selectedFile.value = event.target.files[0];
    };


    const selectFile = () => {
      fileInput.value.click();
    };


    const submitPhoto = async () => {
      if (!selectedFile.value) {
        console.error("No file selected.");
        return;
      }

      const formData = new FormData();
      formData.append('image', selectedFile.value);

      try {
        const response = await axios.post('/user-foto/', formData, {
          headers: {
            'Authorization': `Bearer ${userStore.user.access}`,
          }
        });
        toastStore.showToast(5000, 'Фотография успешно загружена!', 'bg-emerald-500');
        console.log("Photo uploaded successfully:", response.data);

        // Предполагается, что response.data содержит URL загруженного изображения.
        userStore.setAvatar(response.data.get_image); // Устанавливаем URL в хранилище

        selectedFile.value = null; // Очистка файла после загрузки
      } catch (error) {
        console.error("Ошибка при загрузке фотографии:", error);
      }
    };

    
    const fetchPhotos = async () => {
      try {
        const response = await axios.get('/user-foto/', {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${userStore.user.access}`,
          },
        });
        photos.value = response.data; 
      } catch (error) {
        console.error('Ошибка при получении фотографий:', error);
      }
    };

    const deletePhoto = async (photoId) => {
      try {
        const response = await axios.delete(`/user-foto/${photoId}/`, {
          headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Bearer ${userStore.user.access}`,
          }
        });
        photos.value = photos.value.filter(photo => photo.id !== photoId);
        toastStore.showToast(5000, 'Фотография успешно удалена!', 'bg-red-500');
        userStore.removeAvatar(response.data.get_image);
        closeModal();
        console.log("Photo deleted successfully");
      } catch (error) {
        console.error("Ошибка при удалении фотографии:", error);
      }
    };

    const nextSlide = () => {
      if (currentIndex.value < photos.value.length - 1) {
        currentIndex.value++;
      } else {
        currentIndex.value = 0;
      }
    };

    const prevSlide = () => {
      if (currentIndex.value > 0) {
        currentIndex.value--;
      } else {
        currentIndex.value = photos.value.length - 1;
      }
    };

    const openModal = (index) => {
      currentPhotoIndex.value = index;
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
    };

    onMounted(fetchPhotos);

    return {
      user: props.user,
      handleFileChange,
      selectFile,
      submitPhoto,
      fileInput,
      deletePhoto,
      photos,
      selectedFile,
      currentIndex,
      nextSlide,
      prevSlide,
      openModal,
      closeModal,
      isModalOpen,
      currentPhotoIndex,
    };
  }
};
</script>

<style lang="css" scoped>
</style>
