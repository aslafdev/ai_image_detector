import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import ModelRunner from '@/views/ModelRunner.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // Modele (Wspólny widok)
    {
      path: '/model/:id',
      name: 'model',
      component: ModelRunner
    },
    // Narzędzia (Osobne widoki - dynamic import dla optymalizacji)
    {
      path: '/tools/fft',
      name: 'tool-fft',
      component: () => import('@/views/tools/FftView.vue')
    },
    {
      path: '/tools/exif',
      name: 'tool-exif',
      component: () => import('@/views/tools/ExifView.vue')
    }
  ]
});

export default router;