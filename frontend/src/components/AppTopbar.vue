<template>
    <Toolbar class="layout-topbar">
        <template #start>
            <div class="topbar-start">
                <Button 
                    icon="pi pi-bars" 
                    text 
                    rounded 
                    class="mr-3"
                    @click="$emit('toggle-sidebar')" 
                />
                
                <div class="title-container">
                    <span class="sub-title">PANEL STEROWANIA</span>
                    <span class="main-title">{{ currentModelName || 'Strona Główna' }}</span>
                </div>
            </div>
        </template>

        <template #end>
            <Button 
                label="Pamięć RAM" 
                icon="pi pi-server" 
                severity="secondary" 
                outlined
                @click="showMemoryDialog = true"
            />
        </template>
    </Toolbar>

    <Dialog v-model:visible="showMemoryDialog" modal header="Zarządzanie Pamięcią" :style="{ width: '30rem' }">
        <p>Tu będzie lista modeli do odładowania.</p>
        <template #footer>
            <Button label="Zamknij" text @click="showMemoryDialog = false" />
        </template>
    </Dialog>
</template>

<script setup>
import { ref } from 'vue';
import Toolbar from 'primevue/toolbar';
import Button from 'primevue/button';
import Dialog from 'primevue/dialog';

defineProps(['currentModelName']);
defineEmits(['toggle-sidebar']);

const showMemoryDialog = ref(false);
</script>

<style scoped>
.layout-topbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4rem; /* 64px */
    z-index: 2000; /* Musi być nad Drawerem */
    
    border: none;
    border-bottom: 1px solid var(--p-content-border-color);
    background: var(--p-surface-0);
    padding: 0 1.5rem;
    border-radius: 0;
}

/* CSS zamiast PrimeFlex */
.topbar-start {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.title-container {
    display: flex;
    flex-direction: column;
}

.sub-title {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--p-text-muted-color);
    text-transform: uppercase;
}

.main-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--p-primary-color);
}
</style>