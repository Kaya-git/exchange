import {createRouter, createWebHistory} from 'vue-router';

export default new createRouter({
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
          component: () => import("./components/User/AccountView")
        },
        {
          name: 'ConfirmExchange',
          path: '/confirm/',
          props: true,
          component: () => import("./components/Exchange/ConfirmExchange")
        },
        {
          name: 'PayRequest',
          path: '/request/',
          component: () => import("./components/Exchange/PayRequest")
        },
    ]
  });