<template>
    <nav class="header-main__nav">
      <ul class="header-main__nav-list nav-list">
        <template v-for="item in navItems" :key="item.id">
            <li v-if="curRoute != item.link" class="nav-list__item">
                <Router-link :to="item.link">
                    {{item.text}}
                </Router-link>
            </li>
          </template>
      </ul>
    </nav>
  </template>
  
  <script>
  import {defineComponent} from 'vue';
  export default defineComponent({
    name: 'NavMenu',
  
    data: () => ({
      navItems: [
        {
            link: '/',
            text: 'Обмен'
        },
        {
            link: '/privacy/',
            text: 'Соглашение'
        },
        {
            link: '/reserves/',
            text: 'Резервы'
        },
        {
            link: '/tariffs/',
            text: 'Тарифы'
        },
        {
            link: '/faq/',
            text: 'FAQ'
        },
        {
            link: '/reviews/',
            text: 'Отзывы'
        },
        {
            link: '/contacts/',
            text: 'Контакты'
        },
      ],
    }),
    computed: {
        curRoute() {
            return this.$route.path;
        }
    }
  });
  </script>
  