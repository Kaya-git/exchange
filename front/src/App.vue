<template>
    <v-app id="app-wrapper" class="app-wrapper">
        <v-container class="app-container">
            <header-view></header-view>
            <main class="page">
                <div class="page__wrapper">
                    <div class="page__content">
                        <router-view></router-view>
                    </div>
                </div>
            </main>
            <footer-view></footer-view>
        </v-container>
    </v-app>
</template>

<script>
import {defineAsyncComponent} from 'vue';
import {mapActions, mapMutations, mapGetters} from 'vuex';
import {getCookie} from '@/helpers';
// import NET from 'vanta/dist/vanta.net.min';
// import * as THREE from 'three';

export default {
    name: 'App',
    components: {
        HeaderView: defineAsyncComponent({
            loader: () => import("./components/Header/HeaderView"),
        }),
        FooterView: defineAsyncComponent({
            loader: () => import("./components/Footer/FooterView"),
        }),
    },
    data() {
        return {
            vantaEffect: null,
        }
    },
    created() {

        this.getApiUUID();
        this.loadDataFromLocalStorage();
    },
    mounted() {
        // window.onload = () => {
        //     this.vantaEffect = NET({
        //         el: '#app-wrapper',
        //         THREE:THREE,
        //         color: 0xff4484,
        //         mouseControls: true,
        //         touchControls: true,
        //         gyroControls: false,
        //         minHeight: 200.00,
        //         minWidth: 200.00,
        //         scale: 1.00,
        //         scaleMobile: 1.00
        //     });
        // };
        if (getCookie('user_email')) {
            this.setUserEmail(getCookie('user_email'));
        }
        this.checkAuth();
        this.whereAmI().then(() => {
            if (this.getCurExchangeStep && localStorage.getItem('startTime')) {
                // router.push({
                //     name: 'ExchangeSteps',
                // })
            }
        });

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
            'setUserEmail'
        ]),
    },
    computed: {
        ...mapGetters([
            'getUuid',
            'getCurExchangeStep',
        ])
    }
}
</script>