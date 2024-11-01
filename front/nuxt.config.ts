// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({


  
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  modules: [
    '@pinia/nuxt',
  ],
  postcss: {
    plugins: {
      
      tailwindcss: {},
      autoprefixer: {},
      
    },
    
  },
  plugins: [
    { src: '~/plugins/luxon.js' },
    { src: '~/plugins/fontawesome.js' },
  ],

  runtimeConfig: {


    public: {
      // clientIdYandex: process.env.CLIENT_ID_YANDEX,
      // clientIdVK: process.env.CLIENT_ID_VK,
      // stripeKey: process.env.STRIPE_KEY
    },
  },
  // head: {

  //   script: [

  //     { src: 'https://js.stripe.com/v3/', async: true, defer: true },

  //   ],

  // },
 
})
