import { createApp, Teleport } from 'vue';
import { createPinia } from 'pinia';
// import './style.css';
import './assets/css/bootstrap.min.css';
import './assets/js/bootstrap.min.js';
import App from './App.vue';
import router from './router/index.js';

const pinia = createPinia();
createApp(App)
.use(router)
.use(pinia)
// .use(Teleport)
.mount('#app');
