<template>
        <v-app id="app-wrapper"  class="app-wrapper">
            <v-container class="app-container">
                <header-view></header-view>
                <main class="page">
                    <div class="page__wrapper">
                        <div class="page__content">
                            <router-view
                                @toggle-wait-modal="toggleWaitModal"
                            ></router-view>
                        </div>
                    </div>
                </main>
                <footer-view></footer-view>
                <wait-modal
                    :model-value="wait"
                ></wait-modal>
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
            loader: () => import("./components/Header/HeaderView"),
        }),
        FooterView: defineAsyncComponent({
            loader: () => import("./components/Footer/FooterView"),
        }),
        WaitModal: defineAsyncComponent({
            loader: () => import("./components/Modal/WaitModal"),
        }),
        // StatusModal: defineAsyncComponent({
        //     loader: () => import("./components/Modal/StatusModal"),
        // }),
    },
    data() {
        return {
            wait: false,
        }
    },
    created() {
        if (getCookie('user_email')) {
            this.setUserEmail(getCookie('user_email'));
        }
        this.getApiUUID().then(() => {
            this.ttl().then(() => {
                if (this.getRequestFixedTime > 0) {
                    this.whereAmI().then(() => {
                        if (this.getCurExchangeStep ) {
                            this.$router.push({
                                name: 'ExchangeSteps',
                            })
                        }
                    });
                }
            });
        });
        this.loadDataFromLocalStorage();
        this.checkAuth();
    },
    mounted() {
        this.setVantaEffect();
        let vm = this;
        window.addEventListener('load',() => {
            vm.loaded();
            vm.resizeBg();
        });
        window.addEventListener('resize', () => {
            vm.resizeBg();
        });
    },
    methods: {
        ...mapActions([
            'getApiUUID',
            'loadDataFromLocalStorage',
            'checkAuth',
            'whereAmI',
            'resizeBg',
            'startCounter',
            'ttl',
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
        }
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