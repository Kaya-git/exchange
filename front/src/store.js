import Vuex from 'vuex';
import {getCookie, deleteCookie, prepareData} from '@/helpers';
import NET from 'vanta/dist/vanta.net.min';

const Store = new Vuex.Store({
    state: {
        exchangeData: null,
        curExchangeStep: null,
        isAuth: false,
        verificationFile: null,
        uuid: null,
        user: {
            email: null,
            orders: [],
            data: {},
        },
        requestFixedTime: 600,
        vantaEffect: null,
        timer: null,
    },
    mutations: {
        setExchangeData(state, data) {
            state.exchangeData = data;
        },
        setVerificationFile(state, data) {
            state.verificationFile = data;
        },
        auth(state) {
            state.isAuth = true;
        },
        setUUID(state, uuid) {
            state.uuid = uuid;
        },
        setLocalStorageData(state) {
            localStorage.setItem('exchangeData', state.exchangeData);
        },
        setUserEmail(state, data) {
            state.user.email = data;
        },
        setCurExchangeStep(state, data) {
            state.curExchangeStep = data;
        },
        setRequestFixedTime(state, data) {
            state.requestFixedTime = data;
        },
        setVantaEffect(state) {
            state.vantaEffect = NET({
                el: '#app-wrapper',
                color: 0xff4484,
                mouseControls: true,
                touchControls: true,
                gyroControls: false,
                minHeight: window.innerHeight,
                minWidth: 200.00,
                scale: 1.00,
                scaleMobile: 1.00
            });
        },
        setUserOrders(state, data) {
            state.user.orders = data;
        },
        setUserData(state, data) {
            state.user.data = data;
        },
    },
    actions: {
        loadDataFromLocalStorage({ commit }) {
            const data = JSON.parse(localStorage.getItem('exchangeData'));
            if (data) {
                commit('setExchangeData', data);  // Вызов мутации setExchangeData для обновления состояния
            }
        },
        async startCounter({ state }) {
            state.timer = true;
            while (state.requestFixedTime > 0 && state.timer) {
                await new Promise(resolve => setTimeout(resolve, 1000));
                if (state.timer)
                    state.requestFixedTime--;
            }
            state.timer = false;
        },
        resetRequestTime({ state }) {
            state.requestFixedTime = 600;
            state.timer = false;
        },
        clearDataFromLocalStorage() {
            localStorage.removeItem('exchangeData');
            if (localStorage.getItem('startTime')) {
                localStorage.removeItem('startTime');
            }
        },
        async checkAuth({commit, state}) {
            if (state.user.email) {
                let response = await fetch('/api/lk/user');
                if (response.ok) {
                    let result = await response.json();
                    await commit('auth');
                    await commit('setUserData', result);
                    return state.isAuth;
                } else {
                    if (getCookie('user_email')) {
                        deleteCookie('user_email');
                    }
                }
            }
        },
        async getApiUUID({commit}) {
            if (getCookie('user_uuid')) {
                commit('setUUID', getCookie('user_uuid'));
            } else {
                let response = await fetch('/api/uuid', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'accept': 'application/json',
                    }
                });
                commit('setUUID', await response.json());
            }
        },
        async whereAmI({commit, state}) {
            let details = {
                'user_uuid': state.uuid,
            }

            let formBody = prepareData(details);

            let response = await fetch('/api/where_am_i/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept':  'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                commit('setCurExchangeStep', await response.json());
            }
        },
        async logout() {
            let response = await fetch('/api/auth/jwt/logout', {
                method: 'POST',
                headers: {
                    'accept':  'application/json',
                },
            });
            if (response.ok) {
                localStorage.removeItem('auth');
                if (getCookie('user_email')) {
                    deleteCookie('user_email');
                }
                location.reload();
            }
        },
        resizeBg({state}) {
            setTimeout(() => {
                state.vantaEffect.resize();
            }, 100);
        },
    },
    getters: {
        getExchangeData: state => state.exchangeData,
        getVerificationFile: state => state.verificationFile,
        getAuthState: state => state.isAuth,
        getUuid: state => state.uuid,
        getCurExchangeStep: state => state.curExchangeStep,
        getUserOrders: state => state.user.orders,
        getUserData: state => state.user.data,
    }
});


Store.watch(
    (state) => state.exchangeData,
    (newValue) => {
        localStorage.setItem('exchangeData', JSON.stringify(newValue))
    },
    { deep: true }
)
export default Store;