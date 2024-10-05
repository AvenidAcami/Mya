import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import Protected from '../components/Protected.vue';
import Login from '../components/Login.vue';

const routes = [
    { path: '/', component: Home },
    // { path: '/home', component: Home },
    { path: '/protected', component: Protected }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
