<template>
    <div class="confirm pt-8 px-2">
        <v-sheet rounded class="confirm__sheet pa-3">
            <v-container fluid class="confirm__container">
                <v-row class="confirm__row">
                    <h2 class="confirm__title title title_h2 title_black mb-4 text-center">Подтвердите создание заявки</h2>
                </v-row>
                <v-row class="confirm__row">
                    <p class="confirm__text text-center">Внимательно проверьте правильность заполненных данных!</p>
                </v-row>
                <v-row class="confirm__row">
                    <v-sheet class="confirm__table-sheet" rounded>
                        <v-table class="confirm__table request-table mb-3">
                            <tbody>
                                <tr>
                                    <td class="request-table__item text-right">Направление обмена</td>
                                    <td class="request-table__item">
                                        {{exchangeData.selectedGiveCurrency}} {{exchangeData.giveTikker}} / {{exchangeData.selectedGetCurrency}} {{exchangeData.getTikker}}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Обмен по курсу</td>
                                    <td class="request-table__item">
                                        {{ exchangeData.give }} {{exchangeData.giveTikker}} = {{ exchangeData.get }} {{exchangeData.getTikker}}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Отправляете</td>
                                    <td class="request-table__item">{{ exchangeData.give }} {{exchangeData.giveTikker}}</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Получаете</td>
                                    <td class="request-table__item">{{ exchangeData.get }} {{exchangeData.getTikker}}</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Номер вашей карты</td>
                                    <td class="request-table__item">{{ exchangeData.cardNumber}}</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Ваш крипто кошелек</td>
                                    <td class="request-table__item">{{ exchangeData.cryptoNumber }}</td>
                                </tr>
                                <tr>
                                    <td class="request-table__item text-right">Ваш email</td>
                                    <td class="request-table__item">{{ exchangeData.email }}</td>
                                </tr>
                            </tbody>
                        </v-table>
                    </v-sheet>
                </v-row>
                <v-row class="confirm__row mb-8 flex-column align-center">
                    <p class="confirm__text text-center mb-4">
                        Курс зафиксирован на 10 минут, до отмены подтверждения заявки:
                    </p>
                    <timer-view :custom-class="'confirm__timer'" :init="600" :route="ExchangeView"></timer-view>
                </v-row>
                <v-row class="confirm__row">
                    <Router-link to="/request/">
                        <v-btn color="success" class="confirm__btn" size="large">Создать заявку</v-btn>
                    </Router-link>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import { mapGetters } from 'vuex';

export default defineComponent({
    name: 'ConfirmExchange',

    data: () => ({
        exchangeData: null,


    }),
    created() {
        this.exchangeData = this.getExchangeData;
    },
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("../Utils/TimerView"),
        }),
    },
    methods: {
        
    },
    computed: {
        ...mapGetters([
            'getExchangeData'
        ]),
    }
});
</script>
