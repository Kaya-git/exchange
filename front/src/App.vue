<template>
        <v-app class="app-wrapper">
            <div id="app-wrapper" class="parallax"></div>
            <v-container class="app-container">
                <HeaderView></HeaderView>
                <main class="page">
                    <div class="page__wrapper">
                        <div class="page__content">
                            <RouterView></RouterView>
                        </div>
                    </div>
                </main>
                <FooterView></FooterView>
                <WaitModal
                    :model-value="wait"
                ></WaitModal>
            </v-container>
        </v-app>
</template>

<script>
import {defineAsyncComponent} from 'vue';
import {mapActions, mapMutations, mapGetters} from 'vuex';
import {getCookie} from '@/helpers';

export default {
    name: 'App',
    components: {
        HeaderView: defineAsyncComponent({
            loader: () => import("@/components/Header/HeaderView"),
        }),
        FooterView: defineAsyncComponent({
            loader: () => import("@/components/Footer/FooterView"),
        }),
        WaitModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/WaitModal"),
        }),
    },
    data() {
        return {
            wait: true,
        }
    },
    created() {
        if (getCookie('user_email')) {
            this.setUserEmail(getCookie('user_email'));
        }
        this.getApiUUID();
        this.loadDataFromLocalStorage();
        this.checkAuth();
        this.requestRecaptchaPublicKey();
    },
    mounted() {
        this.setVantaEffect();
        let vm = this;
        window.addEventListener('load',() => {
            vm.loaded();
            vm.wait = false;
        });
    },
    methods: {
        ...mapActions([
            'getApiUUID',
            'loadDataFromLocalStorage',
            'checkAuth',
            'whereAmI',
            'requestRecaptchaPublicKey',
            'startCounter',
            'ttl',
            'getStatus',
        ]),
        ...mapMutations([
            'setUserEmail',
            'setVantaEffect',
            'setLoaded',
        ]),
        toggleWaitModal() {
            this.wait = !this.wait;
        },
        loaded() {
            let body = document.querySelector('body');
            body.classList.add('loaded');
            this.setLoaded();
        },
    },
    computed: {
        ...mapGetters([
            'getUuid',
            'getCurExchangeStep',
            'getRequestFixedTime',
        ]),
    },
}
</script>