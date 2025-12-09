import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '@/services/api'; // Importujemy nasz serwis

export const useModelsStore = defineStore('models', () => {
    
    // STAN (State)
    const availableModels = ref([]); 
    const isLoading = ref(false);    
    const error = ref(null);         // Czy wystąpił błąd?

    // 2. NARZĘDZIA (Pozostają hardcoded, bo to widoki frontendowe)
    const availableTools = ref([
        { id: 'fft', name: 'Analiza FFT', icon: 'pi pi-chart-bar', route: '/tools/fft' },
        { id: 'exif', name: 'Przeglądarka EXIF', icon: 'pi pi-image', route: '/tools/exif' },
        { id: 'hex', name: 'Podgląd Hex', icon: 'pi pi-code', route: '/tools/hex' }
    ]);

    // AKCJE (Actions)
    async function fetchModels() {
        isLoading.value = true;
        error.value = null;
        
        try {
            // Wywołujemy Axios
            const response = await api.getModels();
            
            availableModels.value = response.data;
            
            console.log("Pobrano modele:", response.data);
            
        } catch (err) {
            console.error("Błąd pobierania modeli:", err);
            error.value = "Nie udało się połączyć z serwerem.";
            
            availableModels.value = [];
        } finally {
            isLoading.value = false;
        }
    }

    const getCurrentPageTitle = (routeId, fullPath) => {
        if (routeId) {
            const model = availableModels.value.find(m => m.id === routeId);
            if (model) return model.name;
        }
        const tool = availableTools.value.find(t => t.route === fullPath);
        if (tool) return tool.name;
        return null;
    };

    return { 
        availableModels, 
        availableTools, 
        isLoading, 
        error, 
        fetchModels,      // Eksportujemy funkcję
        getCurrentPageTitle 
    };
});