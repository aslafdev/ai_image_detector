import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';

import './assets/main.css';

import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';

import 'primeicons/primeicons.css';
import Ripple from 'primevue/ripple';
import Tooltip from 'primevue/tooltip';

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            darkModeSelector: false, // Wymuszony tryb jasny
        }
    },
    ripple: true // Włączamy efekt "fali"
});

app.directive('ripple', Ripple);
app.directive('tooltip', Tooltip);

app.mount('#app');