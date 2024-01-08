<template>
    <div class="error-page">
        <v-sheet rounded class="error-page__sheet pa-3 rounded-t-0">
            <v-container fluid class="error-page__container">
                <v-row class="error-page__row">
                    <h2 class="error-page__title title title_h2 title_black mb-4 text-center">{{title}}</h2>
                </v-row>
                <v-row class="error-page__row">
                    <p class="error-page__text text-center">{{subtitle}}</p>
                </v-row>
                <v-row class="error-page__row">
                    <v-sheet class="error-page__table-sheet" rounded>
                        <v-table class="error-page__table request-table mb-3">
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
                <v-row>
                    <v-col class="d-flex justify-center">
                        <RouterLink to="/">
                            <v-btn size="large" color="success">На главную</v-btn>
                        </RouterLink>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>
<script>
import {defineComponent} from 'vue';
import { mapGetters } from 'vuex';

export default defineComponent({
    name: 'SuccessView',
    props: {
        subtitle: {
            type: String,
            default: '',
        },
        title: {
            type: String,
            default: '',
        },
    },
    data: () => ({
        exchangeData: null,
    }),
    created() {
        this.exchangeData = this.getExchangeData;
    },
    components: {

    },
    methods: {

    },
    computed: {
        ...mapGetters([
            'getExchangeData',
        ]),
    }
});
</script>
