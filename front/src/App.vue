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
        this.getApiUUID();
        this.loadDataFromLocalStorage();
        this.checkAuth();
    },
    mounted() {
        this.setVantaEffect();
        this.whereAmI().then(() => {
            if (this.getCurExchangeStep && localStorage.getItem('startTime')) {
                // router.push({
                //     name: 'ExchangeSteps',
                // })
            }
        });

        fetch('/api/redis/ttl' + '?user_uuid=' + this.getUuid);

        this.startCounter();
    },
    methods: {
        ...mapActions([
            'getApiUUID',
            'loadDataFromLocalStorage',
            'checkAuth',
            'whereAmI',
            'startCounter',
        ]),
        ...mapMutations([
            'setUserEmail',
            'setVantaEffect'
        ]),
        toggleWaitModal() {
            this.wait = !this.wait;
        },
    },
    computed: {
        ...mapGetters([
            'getUuid',
            'getCurExchangeStep',
        ]),
    },
}
</script>