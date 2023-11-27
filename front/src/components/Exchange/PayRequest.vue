<template>
    <div class="request pt-8 px-2">
        <v-sheet rounded class="request__sheet pa-3">
            <v-container class="request__container">
                <v-row class="request__row">
                    <h2 class="request__title title title_h2 title_black">Оплатить заявку # 244544</h2>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-sheet class="request__table-sheet" rounded>
                        <v-table class="request__table request-table ">
                            <tbody>
                                <tr>
                                    <td class="request-table__item text-right">Направление обмена</td>
                                    <td class="request-table__item">Сбербанк RUB / Dogecoin DOGE</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Обмен по курсу</td>
                                    <td class="request-table__item">30000 RUB = 150 DOGE</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Отправляете</td>
                                    <td class="request-table__item">30000 RUB</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Получаете</td>
                                    <td class="request-table__item">150 DOGE</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Номер вашей карты</td>
                                    <td class="request-table__item">4556 1243 2222 0942</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Ваш крипто кошелек</td>
                                    <td class="request-table__item">D95REFRGERGEFRGERGERGE</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Ваш email</td>
                                    <td class="request-table__item">text@test.ru</td>
                                </tr>
                            </tbody>
                        </v-table>
                    </v-sheet>
                </v-row>
                <v-row class="request__row mb-2"> 
                    <p class="request__text">Курс зафиксирован на 15 минут. Заявка отменится через:</p>
                </v-row>
                <v-row class="request__row mb-8">
                    <timer-view :custom-class="'request__timer'" :init="900"></timer-view>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-expansion-panels>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                Шаг 1. Переведите {{exchangeData.give}} {{exchangeData.giveTikker}} c указанной карты
                            </v-expansion-panel-title>
                        </v-expansion-panel>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                Шаг 2. После перевода нажмите на кнопку "Оплачено"
                            </v-expansion-panel-title>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-col class="d-flex justify-end">
                        <v-btn id="request-submit" size="large" color="success" @click="toggleWaitOverlay()">
                            Оплачено
                        </v-btn>
                    </v-col>
                    <v-col>
                        <Router-link to="/">
                            <v-btn size="large" color="error">Отменить</v-btn>
                        </Router-link>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
    <template v-if="getWaitOverlayState">
        <confirm-wait :model-value="getWaitOverlayState"></confirm-wait>
    </template>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import { mapGetters, mapMutations } from 'vuex';

export default defineComponent({
    name: 'PayRequest',

    data: () => ({
        exchangeData: null,
        overlay: false,
    }),
    created() {
        this.exchangeData = this.getExchangeData;
    },
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("../Utils/TimerView"),
        }),
        ConfirmWait: defineAsyncComponent({
            loader: () => import("../Modal/ConfirmWait"),
        }),
    },
    methods: {
        ...mapMutations ([
            'openWaitOverlay',
            'toggleWaitOverlay'
        ])
    },
    computed: {
        ...mapGetters([
            'getExchangeData',
            'getWaitOverlayState',
        ]),
    }
});
</script>
