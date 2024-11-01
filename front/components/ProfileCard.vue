<template>
<div class="flex space-x-4 items-center p-4">
  <div class="flex mr-auto items-center space-x-4">
        <img  v-if="user.avatar" :src="user.avatar" class="w-56 h-56 shrink-0 rounded-full" />
        <img  v-else src="@/assets/img/default.png" class="w-56 h-56 shrink-0 rounded-full" />

        <div class="space-y-2 flex flex-col flex-1 truncate text-gray-500">
          <strong class="truncate">{{ user.username }}</strong>
          
          <p class="font-normal text-base leading-tight truncate">{{ user.first_name }} {{ user.last_name }}</p>
          <strong class="font-normal text-base leading-tight truncate">{{ user.email }}</strong>
          <p class="font-normal text-base leading-tight truncate">{{ user.bio }}</p>

          <div class="inline-flex  items-center space-x-2"  v-if="user.active">
            <svg 
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              fill="currentColor"
              class="w-6 h-6 text-yellow-500"
            > 
              <path d="M12 .587l3.668 7.568 8.332 1.144-6.004 5.547 1.412 8.208L12 18.896l-7.408 3.883 1.412-8.208-6.004-5.547 8.332-1.144L12 .587z"/>
            
            </svg> 
            <span> Бизнес аккаунт </span>
            
          </div>
        </div>
  </div>
</div>

</template>

<script>
export default {
  name: 'ProfileCard',
  props: {
    user: Object,
  },
};
</script>
