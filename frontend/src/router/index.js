import { createRouter, createWebHistory } from 'vue-router'
import Main from "../components/Main.vue";
import Login from "../components/Login.vue";
import { useUserStore } from '../store/user';
import Register from '../components/Register.vue';
import Activation from "../components/Activation.vue";
import Animaltypes from "../components/Animaltypes.vue";
import AnimaltypesForm from "../components/AnimaltypesForm.vue";
import Breeds from "../components/Breeds.vue";
import BreedsForm from "../components/BreedsForm.vue";
import Animals from "../components/Animals.vue";
import AnimalsForm from "../components/AnimalsForm.vue";
import Weightings from "../components/Weightings.vue";
import WeightingsForm from "../components/WeightingsForm.vue";

const routes = [
    {
        path: '/',
        name: 'Main',
        component: Main,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/login',
        name: 'Login',
        component: Login,
        beforeEnter: (to, from, next) => {
            // Install the user store
            const userStore = useUserStore();
            // Redirect if user is authenticated
            if (userStore.userIsAuth === true) {
                return next('/');
            }
            // Allow route entry if user is not authenticated
            return next();
        }
    },
    {
        path: '/register',
        name: 'Register',
        component: Register,
        beforeEnter: (to, from, next) => {
            // Install the user store
            const userStore = useUserStore();
            // Redirect if user is authenticated
            if (userStore.userIsAuth === true) {
                return next('/');
            }
            // Allow route entry if user is not authenticated
            return next();
        }
    },
    {
        path: '/users/activation/:uid/:token',
        name: 'Activation',
        component: Activation,
        beforeEnter: (to, from, next) => {
            // Install the user store
            const userStore = useUserStore();
            // Redirect if user is authenticated
            if (userStore.userIsAuth === true) {
                return next('/');
            }
            // Allow route entry if user is not authenticated
            return next();
        }
    },
    {
        path: '/animaltypes/page/:page',
        name: 'Animaltypes',
        component: Animaltypes,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/animaltypes/add',
        name: 'AnimaltypesFormAdd',
        component: AnimaltypesForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/animaltypes/edit/:id',
        name: 'AnimaltypesFormEdit',
        component: AnimaltypesForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/breeds/page/:page',
        name: 'Breeds',
        component: Breeds,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/breeds/add',
        name: 'BreedsFormAdd',
        component: BreedsForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/breeds/edit/:id',
        name: 'BreedsFormEdit',
        component: BreedsForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/animals/page/:page',
        name: 'Animals',
        component: Animals,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/animals/add',
        name: 'AnimalsFormAdd',
        component: AnimalsForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/animals/edit/:id',
        name: 'AnimalsFormEdit',
        component: AnimalsForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/weightings/page/:page',
        name: 'Weightings',
        component: Weightings,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
    {
        path: '/weightings/:action/:id',
        name: 'WeightingsForm',
        component: WeightingsForm,
        beforeEnter: (to, from, next) => {
            const userStore = useUserStore();
            if (userStore.userIsAuth === false) {
                return next('/login');
            }
            return next();
        }
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;