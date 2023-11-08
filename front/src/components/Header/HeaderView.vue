<template>
  <header class="header">
    <v-container class="header__container">
      <v-row class="header-main">
        <v-col class="header-main__col v-col-2">
            <div class="header-main__logo header-logo">
              <Router-link to="/">Crypto</Router-link>
            </div>
        </v-col>
        <v-col class="v-col-1"></v-col>
        <v-col class="header-main__col v-col-7">
          <nav-menu></nav-menu>
        </v-col>
        <v-col v-if="!isExcludeRoute" class="header-main__col v-col-2 d-flex justify-end pt-4">
          <RouterLink to="/auth/">
            <v-btn 
              class="header-main__auth outlined-btn" 
              variant="outlined"
              size="large"
              >
              <template v-slot:prepend>
                  <span>
                      <img src="/icons/user-circle-o.svg" alt="">
                  </span>
              </template>
              Войти
            </v-btn>
          </RouterLink>
        </v-col>
      </v-row>
      <v-row class="header-mobile justify-space-between">
          <v-col class="v-col-6">
            <div class="header-mobile__logo header-logo">
              <Router-link to="/">Crypto</Router-link>
            </div>
          </v-col>
      </v-row>
    </v-container>
  </header>
  <nav-mobile></nav-mobile>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
export default defineComponent({
  name: 'HeaderView',
  data: () => ({
    
  }),
  components: {
      NavMenu: defineAsyncComponent({
        loader: () => import("../Navigation/NavMenu"),
      }),
      NavMobile: defineAsyncComponent({
        loader: () => import("../Navigation/NavMobile"),
      }),
  },
  methods: {
  },
  computed: {
      curRoute() {
          return this.$route.path;
      },
      isExcludeRoute() {
        const excluded = ['/auth/', '/register/'];
        if (excluded.includes(this.curRoute)) {
          console.log(this.curRoute);
          return true;
        }
        return false;
    }
  }
});
</script>
