<template>
  <div class="transition-transform duration-200 ease-in-out hover:scale-[1.01]">
    <div class="flex items-center leading-6 space-x-3 py-3 px-4 w-full text-lg text-gray-600 focus:outline-none hover:bg-gray-100 rounded-md" @click="$emit('toggleOrders')">
    <svg class="w-7 h-7" fill="currentColor" viewBox="0 0 24 24">
                <path d="M3 5C3 3.89543 3.89543 3 5 3H9C10.1046 3 11 3.89543 11 5V9C11 10.1046 10.1046 11 9 11H5C3.89543 11 3 10.1046 3 9V5ZM9 5H5V9H9V5Z"/><path d="M3 15C3 13.8954 3.89543 13 5 13H9C10.1046 13 11 13.8954 11 15V19C11 20.1046 10.1046 21 9 21H5C3.89543 21 3 20.1046 3 19V15ZM9 15H5V19H9V15Z"/><path d="M13 5C13 3.89543 13.8954 3 15 3H19C20.1046 3 21 3.89543 21 5V9C21 10.1046 20.1046 11 19 11H15C13.8954 11 13 10.1046 13 9V5ZM19 5H15V9H19V5Z"/><path d="M13 15C13 13.8954 13.8954 13 15 13H19C20.1046 13 21 13.8954 21 15V19C21 20.1046 20.1046 21 19 21H15C13.8954 21 13 20.1046 13 19V15ZM19 15H15V19H19V15Z"/>
    </svg>
      <span>Заказы <span class="text-orange-500">{{ orders.length }}</span></span>
      <svg v-if="showOrders" class="w-4 h-4 transform transition-transform" :class="{'rotate-180': showOrders}" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 16l-4-4h8l-4 4z" />
      </svg>
    </div>
    <ul v-show="showOrders" class="flex flex-col gap-4 pl-2 mt-2">
      <li v-for="order in orders" :key="order.id" class="flex justify-between py-2 px-4 bg-gray-100 rounded-md">
        <div>
        
          <span class="text-gray-500"> Продукт <strong class="text-bold text-orange-500">  {{ order.product_name }} </strong> </span>
          <span class="text-gray-500"> создан {{ formatDate(order.created_at) }} </span>
        </div>

        <button @click="$emit('deleteOrder', order.id)" class="text-red-500">Удалить</button>
        
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'OrdersList',
  props: {
    orders: Array,
    showOrders: Boolean,
  },
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
  },
};
</script>
