<template>
  <div class="container mx-auto p4-10">
    <div class="max-w-md mx-auto bg-white rounded-lg overflow-hidden md:max-w-xl">
      <div class="md:flex">
        <div class="w-full px-6 py-8 md:p-8">
          <h2 class="text-2xl text-gray-400 font-semibold">Редактировать профиль</h2>

          <form @submit.prevent="submitForm" class="mt-6 text-gray-500">
            <div class="mb-6">
              <label class="block  font-bold mb-2 " for="username"
                >Логин</label
              >
              <input
                type="text"
                id="username"
                v-model="formData.username"
                required
                class="shadow appearance-none border rounded w-full py-2 px-3  leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Логин"
              />
            </div>
            <div class="mb-6">
              <label class="block  font-bold mb-2" for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="formData.email"
                required
                class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Email"
              />
            </div>
            <div class="mb-6">
              <label class="block  font-bold mb-2" for="first_name"
                >Имя</label
              >
              <input
                type="text"
                id="first_name"
                v-model="formData.first_name"
                class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Имя"
              />
            </div>

            <div class="mb-6">
              <label class="block  font-bold mb-2" for="last_name"
                >Фамилия</label
              >
              <input
                id="last_name"
                v-model="formData.last_name"
                class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="Фамилия"
              />
            </div>
            <div class="mb-6">
              <label class="block  font-bold mb-2" for="bio">О себе</label>
              <input
                type="text"
                id="bio"
                v-model="formData.bio"
                class="shadow appearance-none border rounded w-full py-2 px-3 leading-tight focus:outline-none focus:shadow-outline"
                placeholder="О себе"
              />
            </div>
            <div class="mb-6">
              <label class="inline-flex items-center">
                <input
                  type="checkbox"
                  v-model="formData.is_trainer"
                  class="form-checkbox"
                />
                <span class="ml-2">Бизнес аккаунт</span>
              </label>
            </div>
            <div class="mb-6">
              <label class="block  font-bold mb-2" for="avatar"
                >Аватар</label
              >
              <input type="file" ref="file" placeholder="Загрузить аватар" />
            </div>

            <template v-if="errors.length > 0">
              <div class="bg-red-300 text-white rounded-lg p-6">
                <p v-for="error in errors" :key="error">{{ error }}</p>
              </div>
            </template>
            <button
              class="bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
              type="submit"
            >
              Изменить
            </button>
            <p class="mt-4 text-gray-600">
              <nuxt-link
                class="text-red-500 hover:underline"
                :to="{ name: 'edit-password' }"
                >Изменить пароль</nuxt-link
              >
            </p>
          </form>
          <button @click="deleteUser" class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">

            Удалить аккаунт

          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useToastStore } from "@/stores/toast";
import { useUserStore } from "@/stores/user";

export default {
  setup() {
    const toastStore = useToastStore();
    const userStore = useUserStore();

    return {
      toastStore,
      userStore,
      formData: {
        email: userStore.user.email,
        username: userStore.user.username,
        first_name: userStore.user.first_name,
        last_name: userStore.user.last_name,
        bio: userStore.user.bio,
        is_trainer: userStore.user.is_trainer,
      },
      errors: [],
    };
  },
  mounted() {
    document.title = "Редактировать профиль | Offer";
  },
  methods: {
    submitForm() {
      this.errors = [];

      if (!this.formData.username.trim()) {
        this.errors.push("Логин обязателен");
      }

      if (!this.formData.email.trim()) {
        this.errors.push("Email обязателен");
      }

      if (this.errors.length === 0) {
        let formData = new FormData();
        formData.append("username", this.formData.username);
        formData.append("email", this.formData.email);
        formData.append("first_name", this.formData.first_name);
        formData.append("last_name", this.formData.last_name);
        formData.append("bio", this.formData.bio);
        formData.append("is_trainer", this.formData.is_trainer);

        if (this.$refs.file.files.length > 0) {
          formData.append("avatar", this.$refs.file.files[0]);
        }

        axios
          .put("/edit-account/", formData)
          .then((response) => {
            this.toastStore.showToast(3000, "Информация сохранена!", "bg-emerald-500");
            this.userStore.setUserInfo({
              id: this.userStore.user.id,
              email: this.formData.email,
              username: this.formData.username,
              first_name: this.formData.first_name,
              last_name: this.formData.last_name,
              bio: this.formData.bio,
              is_trainer: this.formData.is_trainer,
            });
            this.userStore.setAvatar(response.data.avatar);
            this.$router.back();
          })
          .catch((error) => {
            console.log("error", error);
            this.toastStore.showToast(
              3000,
              "Произошла ошибка при сохранении информации!",
              "bg-red-300"
            );
          });
      }
    },
    deleteUser() {
      axios
      .post("/delete-user/")
        .then(() => {
          this.toastStore.showToast(3000, "Пользователь успешно удален!", "bg-red-500");
          this.userStore.removeToken();
          this.$router.push({ name: "login" });
        })
        .catch((error) => {

          console.log("error", error);
          this.toastStore.showToast(3000, "Произошла ошибка при удалении пользователя!", "bg-red-300");
        })
        .finally(() => {
          this.isLoading = false;
        });
    }
  },
};
</script>
