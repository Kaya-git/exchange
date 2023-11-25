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
                    <v-table class="confirm__table request-table mb-3">
                        <tbody>
                            <tr>
                                <td class="request-table-item text-right">Направление обмена</td>
                                <td class="request-table-item">Сбербанк RUB / Dogecoin DOGE</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Обмен по курсу</td>
                                <td class="request-table-item">30000 RUB = 150 DOGE</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Отправляете</td>
                                <td class="request-table-item">30000 RUB</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Получаете</td>
                                <td class="request-table-item">150 DOGE</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Номер вашей карты</td>
                                <td class="request-table-item">4556 1243 2222 0942</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Ваш крипто кошелек</td>
                                <td class="request-table-item">D95REFRGERGEFRGERGERGE</td>
                            </tr>
                            <tr>
                                <td class="request-table-item text-right">Ваш email</td>
                                <td class="request-table-item">text@test.ru</td>
                            </tr>
                        </tbody>
                    </v-table>
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

export default defineComponent({
    name: 'ConfirmExchange',

    data: () => ({
    }),
    mounted() {
        console.log(this.$store.getters.getExchangeData);
    },
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("../Utils/TimerView"),
        }),
    }
});
</script>
