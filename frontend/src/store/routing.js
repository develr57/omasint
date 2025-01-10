import { defineStore } from 'pinia';


export const useRoutingStore = defineStore('routing', {
    state: () => ({
        curr_route_name: null,
        mainActive: false,
        animaltypesActive: false,
        breedsActive: false,
        animalsActive: false,
        weightingsActive: false,
    }),
    getters: {
        getCurrRouteName: state => state.curr_route_name
    },
    actions: {
        setCurrRouteName(name) {
            this.curr_route_name = name;
        },
        setMenuItemActive(route_name) {
            this.mainActive = false;
            this.animaltypesActive = false;
            this.breedsActive = false;
            this.animalsActive = false;
            this.weightingsActive = false;
            if (route_name === 'Main') {
            this.mainActive = true;
            }
            if (route_name === 'Animaltypes') {
            this.animaltypesActive = true;
            }
            if (route_name === 'Breeds') {
            this.breedsActive = true;
            }
            if (route_name === 'Animals') {
            this.animalsActive = true;
            }
            if (route_name === 'Weightings') {
            this.weightingsActive = true;
            }
        }
    }
});