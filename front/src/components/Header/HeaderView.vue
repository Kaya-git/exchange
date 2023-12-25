<template>
    <header class="header">
        <v-container class="header__container">
            <v-row class="header-main">
                <v-col class="header-main__col v-col-2">
                    <div class="header-main__logo header-logo">
                        <Router-link to="/">VVS Coin</Router-link>
                    </div>
                </v-col>
                <v-col class="header-main__col v-col-8">
                    <nav-menu></nav-menu>
                </v-col>
                <v-col v-if="!isExcludeRoute" class="header-main__col v-col-2 d-flex justify-center pt-4">
                    <template v-if="!getAuthState">
                        <RouterLink to="/auth/">
                            <v-btn
                                class="header-main__auth outlined-btn"
                                variant="outlined"
                                size="large">
                                <template v-slot:prepend>
                                  <span>
                                      <img src="/icons/user-circle-o.svg" alt="">
                                  </span>
                                </template>
                                Войти
                            </v-btn>
                        </RouterLink>
                    </template>
                    <template v-else-if="getAuthState && curRoute === '/user/'">
                        <v-btn
                            class="header-main__auth outlined-btn"
                            variant="outlined"
                            size="large"
                            @click.prevent="logout">
                            <template v-slot:prepend>
                              <span>
                                  <img src="/icons/user-circle-o.svg" alt="">
                              </span>
                            </template>
                            Выйти
                        </v-btn>
                    </template>
                    <template v-else-if="getAuthState && curRoute !== '/user/'">
                        <RouterLink to="/user/">
                            <v-btn
                                class="header-main__auth outlined-btn"
                                variant="outlined"
                                size="large">
                                <template v-slot:prepend>
                                  <span>
                                      <img src="/icons/user-circle-o.svg" alt="">
                                  </span>
                                </template>
                                Мой кабинет
                            </v-btn>
                        </RouterLink>
                    </template>
                </v-col>
            </v-row>
            <v-row class="header-mobile justify-space-between">
                <v-col class="v-col-2">
                    <div class="header-mobile__logo header-logo">
                        <Router-link to="/">VVS Coin</Router-link>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </header>
    <nav-mobile></nav-mobile>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters, mapActions} from 'vuex';
export default defineComponent({
    name: 'HeaderView',
    data: () => ({}),
    components: {
        NavMenu: defineAsyncComponent({
            loader: () => import("../Navigation/NavMenu"),
        }),
        NavMobile: defineAsyncComponent({
            loader: () => import("../Navigation/NavMobile"),
        }),
    },
    methods: {
        ...mapActions([
            'logout',
        ]),
    },
    computed: {
        ...mapGetters([
            'getAuthState',
        ]),
        curRoute() {
            return this.$route.path;
        },
        isExcludeRoute() {
            const excluded = ['/auth/', '/register/'];
            if (excluded.includes(this.curRoute)) {
                return true;
            }
            return false;
        }
    }
});
</script>
