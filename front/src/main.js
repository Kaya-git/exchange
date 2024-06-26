import {createApp} from 'vue';
import Vuetify from './plugins/vuetify';
import App from './App.vue';
import Store from './store';
import Router from './router';
import v3ImgPreview from 'v3-img-preview';
import 'vuetify/styles';
import './sass/style.scss';

const app = createApp(App);

app
    .use(Store)
    .use(Router)
    .use(Vuetify)
    .use(v3ImgPreview)
    .mount('#app');