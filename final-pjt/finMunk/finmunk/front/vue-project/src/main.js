// main.js
import { createApp } from 'vue'
import App from './App.vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import router from './router'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)

app.mount('#app')


// // 자동로그인
// import { useUserStore } from '@/stores/user'
// const userStore = useUserStore()
// if (userStore.token && !userStore.user) {
//   userStore.fetchUser()
// }
