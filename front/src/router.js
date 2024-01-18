import {createRouter, createWebHistory} from 'vue-router';
import {nextTick} from 'vue';
import store from './store';

const router = new createRouter({
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
            component: () => import("./components/Exchange/ExchangeSteps"),
            meta: {
                needStep: true,
            }
        },
        {
            name: 'NotFound',
            path: '/:pathMatch(.*)*',
            component: () => import("./components/Pages/NotFound")
        },
    ]
});

// eslint-disable-next-line
router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth) {
        store.dispatch('checkAuth').then((data) => {
            console.log(data);
            console.log(store.state.isAuth);
            if (!store.state.isAuth) {
                next({
                    name: 'AuthView',
                });
            } else {
                next()
            }
        })
    } else if (to.meta.needStep && !store.state.curExchangeStep) {
        next({
            name: 'ExchangeView',
        });
    } else {
        next();
    }
});

const DEFAULT_TITLE = 'Мультивалютный обменный сервис';
const PREFIX = 'VVS Coin - '
router.afterEach((to) => {
    nextTick(() => {
        document.title = PREFIX + (to.meta.title || DEFAULT_TITLE);
        if (store.state.vantaEffect) {
            store.dispatch('resizeBg');
        }
    });
});
export default router;