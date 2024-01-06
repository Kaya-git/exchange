<template>
    <div class="mobile-menu">
        <div class="mobile-menu__wrapper">
            <div class="mobile-menu__ham">
                <svg
                    class="ham ham-rotate ham-ui"
                    viewBox="0 0 100 100"
                    @click="toggleMenu"
                >
                    <path
                        class="line top"
                        d="m 30,33 h 40 c 0,0 9.044436,-0.654587 9.044436,-8.508902 0,-7.854315 -8.024349,-11.958003 -14.89975,-10.85914 -6.875401,1.098863 -13.637059,4.171617 -13.637059,16.368042 v 40"
                    ></path>
                    <path class="line middle" d="m 20,50 h 40"></path>
                    <path
                        class="line bottom"
                        d="m 30,67 h 40 c 12.796276,0 15.357889,-11.717785 15.357889,-26.851538 0,-15.133752 -4.786586,-27.274118 -16.667516,-27.274118 -11.88093,0 -18.499247,6.994427 -18.435284,17.125656 l 0.252538,40"
                    ></path>
                </svg>
            </div>
        </div>
    </div>
    <nav class="mobile-nav">
        <ul class="mobile-nav__list">
            <template v-for="item in navItems" :key="item.id">
                <li class="mobile-nav__item">
                    <Router-link v-if="item.id === 0 && getAuthState" to="/user/" @click="toggleMenu">
                        <span>Мой кабинет</span>
                    </Router-link>
                    <Router-link v-else :to="item.link" @click="toggleMenu">
                        <span>{{ item.text }}</span>
                    </Router-link>
                </li>
            </template>
        </ul>
    </nav>
</template>

<script>
import {defineComponent} from 'vue';
import {mapGetters} from 'vuex';


export default defineComponent({
    name: 'NavMobile',

    data: () => ({
        navItems: [
            {
                link: '/auth/',
                text:  'Войти',
            },
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
    created(){
        if (this.getAuthState){
            this.navItems[0].link = '/user/';
            this.navItems[0].text = 'Мой кабинет';
        }
    },
    methods: {
        toggleScroll() {
            const body = document.querySelector('body');
            body.classList.toggle('_lock');
        },
        toggleMenu() {
            this.toggleScroll();

            const mobileMenu = document.querySelector('.mobile-menu');
            const mobileNav = document.querySelector('.mobile-nav');
            const ham = document.querySelector('.ham');

            mobileMenu.classList.toggle('active');
            mobileNav.classList.toggle('active');
            ham.classList.toggle('active');
        }
    },
    computed: {
        ...mapGetters([
            'getAuthState',
        ]),
        curRoute() {
            return this.$route.path;
        }
    }
});
</script>
  