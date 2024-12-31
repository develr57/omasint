import { defineStore } from 'pinia';


export const useUserStore = defineStore('user', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        storedUser: localStorage.getItem('user') || null,
    }),
    getters: {
        user: state => {
            if (state.storedUser && state.storedUser !== 'undefined') {
                return JSON.parse(state.storedUser);
            }
            return state.storedUser;
        },
        userIsAuth: state => !!state.token,
    },
    actions: {
        storeLoggedInUser(user) {
            const stringifiedUser = JSON.stringify(user);
            localStorage.setItem('user', stringifiedUser);
            this.storedUser = stringifiedUser;
        },
        storeAuthToken(token) {
            localStorage.setItem('token', token);
            this.token = token;
        },
        logoutUser() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.token = null;
            this.storedUser = null;
        }
    }
});