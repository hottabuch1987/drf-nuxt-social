<template>
  <div class="page">
    <AppHeader />
    

    <main class="main mt-12">
      <Toast />

      <slot></slot>
    </main>

    <AppFooter />
  </div>
</template>

<script setup>
import AppHeader from "./components/AppHeader.vue";
import AppFooter from "./components/AppFooter.vue";
import Toast from "./components/Toast.vue";
</script>

<style>
.page {
  display: flex;

  flex-direction: column;

  min-height: 100vh; /* Минимальная высота всего окна */
}

.main {
  flex: 1; /* Увеличивает основной контент, чтобы заполнить пространство */
}
</style>
