import {createRouter, createWebHistory} from 'vue-router';
import {nextTick} from 'vue';

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
            component: () => import("./components/User/AuthView"),
            meta: { title: 'Авторизация' }
        },
        {
            name: 'RegisterView',
            path: '/register/',
            component: () => import("./components/User/RegisterView"),
            meta: { title: 'Регистрация' }
        },
        {
            name: 'ContactsView',
            path: '/contacts/',
            component: () => import("./components/Pages/ContactsView"),
            meta: { title: 'Контакты' }
        },
        {
            name: 'ReviewView',
            path: '/reviews/',
            component: () => import("./components/Pages/ReviewView"),
            meta: { title: 'Отзывы' }
        },
        {
            name: 'FaqView',
            path: '/faq/',
            component: () => import("./components/Pages/FaqView"),
            meta: { title: 'Вопросы и ответы' }
        },
        {
            name: 'PrivacyView',
            path: '/privacy/',
            component: () => import("./components/Pages/PrivacyView"),
            meta: { title: 'Соглашение' }
        },
        {
            name: 'TariffView',
            path: '/tariffs/',
            component: () => import("./components/Pages/TariffView"),
            meta: { title: 'Тарифы' }
        },
        {
            name: 'ReservesView',
            path: '/reserves/',
            component: () => import("./components/Pages/ReservesView"),
            meta: { title: 'Резервы' }
        },
        {
            name: 'AccountView',
            path: '/user/',
            component: () => import("./components/User/AccountView"),
            meta: {
                requiresAuth: true,
                title: 'Личный кабинет',
            },
        },
        {
            name: 'ExchangeSteps',
            path: '/exchange/',
            component: () => import("./components/Exchange/ExchangeSteps")
        },
        {
            name: 'NotFound',
            path: '/:pathMatch(.*)*',
            component: () => import("./components/Pages/NotFound")
        },
    ]
});

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

const DEFAULT_TITLE = 'Мультивалютный обменный сервис';
const PREFIX = 'VVS Coin - '
Router.afterEach((to) => {
    nextTick(() => {
        document.title = PREFIX + (to.meta.title || DEFAULT_TITLE);
    });
});
export default Router;