// plugins/luxon.js
export default defineNuxtPlugin((nuxtApp) => {
    nuxtApp.provide('luxon', {
      formatDate: (date) => {
        return DateTime.fromISO(date).setLocale('ru').toFormat({
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        });
      }
    });
  });
  