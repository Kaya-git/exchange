import Vuex from 'vuex';
import {getCookie, setCookie} from '@/helpers';

const Store = new Vuex.Store({
    state: {
        exchangeData: null,
        curExchangeStep: null,
        isAuth: false,
        verificationFile: null,
        uuid: null,
        user: {
            email: null,
        },
        requestFixedTime: 600,
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
        }
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
            if (state.user.email && !state.isAuth) {
                let body = {
                    'email': state.user.email,
                }
                let response = await fetch('/api/auth/request-verify-token',{
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'accept':  'application/json',
                    },
                    body: JSON.stringify(body),
                });
                if (response.ok) {
                    await commit('auth');
                    localStorage.setItem('auth', 'true');
                    return state.isAuth;
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
            let body = {
                'user_uuid': state.uuid,
            }
            let response = await fetch('/api/where_am_i/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept':  'application/json',
                },
                body: JSON.stringify(body),
            });
            if (response.ok) {
                commit('setCurExchangeStep', await response.json());
            }
        },
        async logout({state}) {
            let response = await fetch('/api/auth/jwt/logout', {
                method: 'POST',
                headers: {
                    'accept':  'application/json',
                },
            });
            if (response.ok) {
                state.isAuth = false;
                if (getCookie('user_email')) {
                    setCookie('user_email', '', 0);
                }
                location.reload();
            }
        },
    },
    getters: {
        getExchangeData: state => state.exchangeData,
        getVerificationFile: state => state.verificationFile,
        getAuthState: state => state.isAuth,
        getUuid: state => state.uuid,
        getCurExchangeStep: state => state.curExchangeStep,
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