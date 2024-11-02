<template>
    <footer class="footer">
            <div class="border border-gray-200 p-2 rounded-md shadow-lg shadow-orange-300">
                <div class="flex items-end gap-1">
                    <!-- <svg
                        class="animate-spin"
                        fill="#F97316"
                        width="50px"
                        height="50px"
                        viewBox="0 0 50 50"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M25 5 C 15 5, 5 15, 5 25 C 5 35, 15 45, 25 45 C 35 45, 45 35, 45 25 C 45 15, 35 5, 25 5 Z 
                                    M25 10 C 30 10, 35 15, 35 25 C 35 35, 30 40, 25 40 C 20 40, 15 35, 15 25 C 15 15, 20 10, 25 10 Z"
                            transform="translate(-5 -5)"
                        />
                    </svg> -->
                    <span class="text-6xl font-semibold text-orange-500">Poster</span> 
                </div>
            </div>
            <span class="sm:text-sm text-xs m-6 text-gray-400">сайт для переписки и общения © 2024</span>
            <span class="sm:text-sm text-xs m-6 text-gray-400">
                <nuxt-link :to="{ name: 'about' }">
                    Политика конфиденциальности | Условия использования
                </nuxt-link>
            </span>  

    </footer>
</template>




