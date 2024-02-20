import Vuex from 'vuex';
import {reactive} from 'vue';
import {getCookie, deleteCookie, prepareData} from '@/helpers';
import NET from 'vanta/dist/vanta.net.min';

const Store = new Vuex.Store({
    state: {
        exchangeData: null,
        curExchangeStep: null,
        curExchangeStatus: null,
        isAuth: false,
        isLoaded: false,
        verificationFile: null,
        uuid: null,
        user: {
            email: null,
            orders: [],
            data: {},
        },
        requestFixedTime: -2,
        vantaEffect: reactive([]),
        recaptchaPublicKey: null,
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
        setLoaded(state) {
            state.isLoaded = true;
        },
        setCurExchangeStatus(state, data) {
            state.curExchangeStatus = data;
        },
        setRecaptchaPublicKey(state, key) {
            state.recaptchaPublicKey = key;
        }
    },
    actions: {
        loadDataFromLocalStorage({ commit }) {
            const data = JSON.parse(localStorage.getItem('exchangeData'));
            if (data) {
                commit('setExchangeData', data);  // Вызов мутации setExchangeData для обновления состояния
            }
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
                } else {
                    if (getCookie('user_email')) {
                        deleteCookie('user_email');
                    }
                }
            }
            return state.isAuth;
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
            return state.curExchangeStep;
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
        async ttl({commit, state}) {
            let response = await fetch('/api/redis/ttl' + '?user_uuid=' + state.uuid);
            if (response.ok) {
                let result = await response.json();
                commit('setRequestFixedTime', result);
            }
        },
        async getStatus({commit, state}) {
            let response = await fetch('/api/orders/get_order_status?user_uuid=' + state.uuid);
            if (response.ok) {
                let result = await response.json();
                if (result.status) {
                    commit('setCurExchangeStatus', result.status);
                }
            }
        },
        async requestRecaptchaPublicKey({commit}){
            let response = await fetch('/api/recaptcha/pbc');
            if (response.ok) {
                let result = await response.json();
                commit('setRecaptchaPublicKey', result);
            }
        },
        async checkToken({state}) {
            let details = {
                'token': state.recaptchaPublicKey,
            }
            let formBody = prepareData(details);
            let response = await fetch('/api/recaptcha/verify-recaptcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept':  'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                let result = await response.json();
                if (result.success) {
                    return true;
                }
            }
            return false;
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
        getRequestFixedTime: state => state.requestFixedTime,
        getCurExchangeStatus: state => state.curExchangeStatus,
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