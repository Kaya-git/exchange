<template>
    <v-app class="app-wrapper">
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
  import { defineAsyncComponent} from 'vue';
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
    data () {
      return {
      }
    },
    methods: {
    },
  }
  </script>