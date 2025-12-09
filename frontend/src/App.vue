<template>
  <div class="app-wrapper">
    <Toast />

    <AppTopbar 
        :currentModelName="currentModelName"
        @toggle-sidebar="isSidebarVisible = !isSidebarVisible" 
    />

    <AppSidebar v-model="isSidebarVisible" />

    <main class="app-main">
      <div class="app-content">
        <RouterView /> 
      </div>
    </main>
      
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRoute } from 'vue-router';
import Toast from 'primevue/toast';
import AppSidebar from '@/components/AppSidebar.vue';
import AppTopbar from '@/components/AppTopbar.vue';
import { useModelsStore } from '@/stores/modelsStore';
import { onMounted } from 'vue';

const isSidebarVisible = ref(false); // Domyślnie schowany na start
const route = useRoute();
const store = useModelsStore();

const currentModelName = computed(() => {
    return store.getCurrentPageTitle(route.params.id, route.path);
});


onMounted(async () => {
    // To wywoła GET /models/
    // Jeśli backend działa -> Sidebar się wypełni i pokaże kropki.
    // Jeśli backend leży -> Console.log błędu (w store), a Sidebar będzie pusty.
    await store.fetchModels();
});



</script>

<style>
/* CSS Reset */
body {
    margin: 0;
    background-color: var(--p-surface-ground);
    font-family: var(--font-family);
    color: var(--p-text-color);
}

.app-wrapper {
    min-height: 100vh;
    padding-top: 4rem; 
}

.app-main {
    width: 100%;
    /* Flexbox do centrowania treści */
    display: flex;
    justify-content: center; 
}

.app-content {
    width: 100%;
    max-width: 1400px;
    padding: 2rem;
}
</style>