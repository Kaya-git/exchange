<template>
    <div class="request pt-8 px-2">
        <v-sheet rounded class="request__sheet pa-3">
            <v-container fluid class="request__container">
                <v-row class="request__row mb-2">
                    <h2 class="request__title title title_black">Оплатить заявку # 244544</h2>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-table class="request__table request-table mb-3">
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
                <v-row class="request__row mb-2"> 
                    <p class="request__text">Курс зафиксирован на 15 минут. Заявка отменится через:</p>
                </v-row>
                <v-row class="request__row mb-2">
                    <timer-view :custom-class="'request__timer'" :init="900"></timer-view>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-expansion-panels>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                Шаг 1. Переведите 30000 RUB c указанной карты
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
                    <v-col>
                        <v-btn size="large" color="success">Оплачено</v-btn>
                    </v-col>
                    <v-col>
                        <v-btn size="large" color="error">Отменить</v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';

export default defineComponent({
    name: 'PayRequest',

    data: () => ({
        
    }),
    mounted() {

    },
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("../Utils/TimerView"),
        }),
    }
});
</script>
