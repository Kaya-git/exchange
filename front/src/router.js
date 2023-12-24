import {createRouter, createWebHistory} from 'vue-router';
import Store from './store';

const Router = new createRouter({
    history: createWebHistory(),
    routes: [
        {
            name: 'ExchangeView',
            path: '/',
            component: () => import("./components/Exchange/ExchangeView")
        },
        {
            name: 'AuthView',
            path: '/auth/',
            component: () => import("./components/User/AuthView")
        },
        {
            name: 'RegisterView',
            path: '/register/',
            component: () => import("./components/User/RegisterView")
        },
        {
            name: 'ContactsView',
            path: '/contacts/',
            component: () => import("./components/Pages/ContactsView")
        },
        {
            name: 'ReviewView',
            path: '/reviews/',
            component: () => import("./components/Pages/ReviewView")
        },
        {
            name: 'FaqView',
            path: '/faq/',
            component: () => import("./components/Pages/FaqView")
        },
        {
            name: 'PrivacyView',
            path: '/privacy/',
            component: () => import("./components/Pages/PrivacyView")
        },
        {
            name: 'TariffView',
            path: '/tariffs/',
            component: () => import("./components/Pages/TariffView")
        },
        {
            name: 'ReservesView',
            path: '/reserves/',
            component: () => import("./components/Pages/ReservesView")
        },
        {
            name: 'AccountView',
            path: '/user/',
            component: () => import("./components/User/AccountView"),
            meta: { requiresAuth: true },
        },
        {
            name: 'ExchangeSteps',
            path: '/exchange/',
            component: () => import("./components/Exchange/ExchangeSteps")
        },
    ]
});
Store.dispatch('checkAuth').then(() => {
    console.log(Store.state.isAuth);
})
// eslint-disable-next-line
Router.beforeEach((to, from) => {
    if (to.meta.requiresAuth && localStorage.getItem('auth') !== 'true') {
        return {
            path: '/auth/',
            // save the location we were at to come back later
            query: { redirect: to.fullPath },
        }
    }
});
export default Router;