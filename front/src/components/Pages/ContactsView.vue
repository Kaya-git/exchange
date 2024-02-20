<template>
    <div class="contacts">
        <v-sheet rounded class="contacts__sheet pa-4">
            <v-container fluid class="contacts__container">
                <v-card class="contacts__card contacts-card pa-4 mb-6">
                    <v-card-item class="contacts-card__item mb-3">
                        <v-card-title class="contacts-card__title">
                            Техническая поддержка клиентов
                        </v-card-title>
                    </v-card-item>
                    <v-card-text class="contacts-card__text">
                        По финансовым и техническим вопросам:
                        <a class="contacts-card__link" href="mailto:vvs.coin777@gmail.com">vvs.coin777@gmail.com</a>
                    </v-card-text>
                </v-card>
                <v-card class="contacts__card contacts-card pa-4 mb-6">
                    <v-card-item class="contacts-card__item mb-3">
                        <v-card-title class="contacts-card__title">
                            Время работы
                        </v-card-title>
                    </v-card-item>
                    <v-card-text class="contacts-card__text">
                        Мы работаем без выходных с 10:00 до 22:00 по московскому времени.
                    </v-card-text>
                </v-card>
                <v-card class="contacts__card contacts-card pa-4 mb-6">
                    <v-card-item class="contacts-card__item mb-3">
                        <v-card-title class="contacts-card__title">
                            Сотрудничество
                        </v-card-title>
                    </v-card-item>
                    <v-card-text class="contacts-card__text">
                        На электронную почту info@gmail.com мы рассматриваем предложения о сотрудничестве исключительно
                        от зарекомендовавших себя компаний, имеющих устоявшуюся многими годами репутацию, положительные,
                        многочисленные, и реальные отзывы от клиентов.
                    </v-card-text>
                </v-card>
                <v-card class="contacts__card contacts-card pa-4 mb-6">
                    <v-card-item class="contacts-card__item mb-3">
                        <v-card-title class="contacts-card__title">
                            Мы на мониторингах
                        </v-card-title>
                    </v-card-item>
                    <v-card-text class="contacts-card__text">
                        <ul class="contacts-card__link-list">
                            <li><a class="contacts-card__link" href="#"><span>BestChange</span></a><span
                                class="contacts-card__divider">|</span></li>
                            <li><a class="contacts-card__link" href="#"><span>kurs.expert</span></a><span
                                class="contacts-card__divider">|</span></li>
                            <li><a class="contacts-card__link" href="#"><span>bits.media</span></a><span
                                class="contacts-card__divider">|</span></li>
                            <li><a class="contacts-card__link" href="#"><span>exnode.ru</span></a></li>
                        </ul>
                    </v-card-text>
                </v-card>
            </v-container>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'ContactsView',

    data: () => ({}),
    mounted() {
    },
    methods: {
    }
});
</script>
