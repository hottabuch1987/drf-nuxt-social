<script setup>
import { useToastStore } from '@/stores/toast'

const store = useToastStore()
</script>

<template>
    <div
        v-if="store.isVisible"
        class="transition ease-in-out delay-500  shadow-2xl opacity-50 px-6 py-6  mb-6 mt-6 text-white  absolute top-2 rounded-xl shadow-xl"
        :class="store.classes"
    >
        {{ store.message }}
    </div>
</template>