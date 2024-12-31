import { defineStore } from 'pinia';


export const useRoutingStore = defineStore('routing', {
    state: () => ({
        curr_route_name: null,
    }),
    getters: {
        getCurrRouteName: state => state.curr_route_name
    },
    actions: {
        setCurrRouteName(name) {
            this.curr_route_name = name;
        }
    }
});