import { defineStore } from 'pinia';


export const useApiStore = defineStore('api', {
    state: () => ({
        API_URL: 'http://127.0.0.1:8000'
    }),
    getters: {

    },
    actions: {

    }
});