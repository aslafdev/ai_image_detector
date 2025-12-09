<template>
    <Drawer 
        v-model:visible="visible" 
        header="Nawigacja" 
        
        :modal="false"
        :dismissable="true"
        :showCloseIcon="true"
        
        class="layout-sidebar-drawer"
    >
        <template #header>
            <div class="sidebar-header">
                <i class="pi pi-compass"></i>
                <span>Nawigacja</span>
            </div>
        </template>

        <div class="sidebar-content">
            
            <div class="nav-section">
                <span class="nav-section-title">Modele AI</span>
                <ul class="nav-list">
                    <li v-for="model in store.availableModels" :key="model.id">
                        <router-link 
                            :to="`/model/${model.id}`" 
                            class="nav-link"
                            active-class="active"
                            v-ripple
                            @click="visible = false" 
                        >
                            <i class="pi pi-box icon"></i>
                            <span class="label">{{ model.name }}</span>
                            
                            <span 
                                class="status-dot" 
                                :class="{ 'loaded': model.status === 'loaded' }"
                                v-tooltip.left="model.status === 'loaded' ? 'W pamięci' : ''"
                            ></span>
                        </router-link>
                    </li>
                </ul>
            </div>

            <div class="separator"></div>

            <div class="nav-section">
                <span class="nav-section-title">Narzędzia</span>
                <ul class="nav-list">
                    <li v-for="tool in store.availableTools" :key="tool.id">
                        <router-link 
                            :to="tool.route" 
                            class="nav-link"
                            active-class="active"
                            v-ripple
                            @click="visible = false"
                        >
                            <i :class="tool.icon + ' icon'"></i>
                            <span class="label">{{ tool.name }}</span>
                        </router-link>
                    </li>
                </ul>
            </div>
        </div>
    </Drawer>
</template>

<script setup>
import { computed } from 'vue';
import Drawer from 'primevue/drawer'; 
import { useModelsStore } from '@/stores/modelsStore';
import { watch } from 'vue';

const store = useModelsStore();
const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);

const visible = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
});

watch(visible, (isOpen) => {
    if (isOpen) {
        // Menu właśnie się otwiera -> odśwież listę w tle
        console.log("Sidebar otwarty -> Odświeżam modele...");
        store.fetchModels(true); // true = tryb cichy (bez spinnera, tylko kropki się zmienią)
    }
});

</script>




<style>
.layout-sidebar-drawer {
    top: 2rem !important; /* Start pod Topbarem */
    height: calc(100% - 4rem) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.04) !important;
    border-right: 1px solid var(--p-content-border-color);
}
</style>

<style scoped>
.sidebar-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--p-primary-color);
}

.sidebar-header i {
    font-size: 1.5rem;
}

.sidebar-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding-top: 1rem;
}

.nav-section {
    margin-bottom: 1rem;
}

.nav-section-title {
    display: block;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--p-text-muted-color);
    padding: 0 1rem 0.5rem 1rem;
    text-transform: uppercase;
}

.nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.nav-link {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    color: var(--p-text-color);
    text-decoration: none;
    transition: background-color 0.2s, color 0.2s;
    border-radius: var(--p-content-border-radius);
    margin: 0 0.5rem 0.25rem 0.5rem;
    cursor: pointer;
}

.nav-link:hover {
    background-color: var(--p-surface-100);
}

.nav-link.active {
    background-color: var(--p-primary-50);
    color: var(--p-primary-color);
    font-weight: 600;
}

.nav-link .icon {
    margin-right: 0.75rem;
    font-size: 1.1rem;
}

.nav-link .label {
    flex: 1; /* Pycha kropkę na prawo */
}

.separator {
    height: 1px;
    background-color: var(--p-content-border-color);
    margin: 1rem 0;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background-color: var(--p-surface-300);
}

.status-dot.loaded {
    background-color: var(--p-green-500);
    box-shadow: 0 0 4px var(--p-green-500);
}
</style>