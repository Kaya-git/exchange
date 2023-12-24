<template>
    <div class="confirm">
        <v-sheet rounded class="confirm__sheet pa-3 rounded-t-0">
            <v-container fluid class="confirm__container">
                <v-row class="confirm__row">
                    <h2 class="confirm__title title title_h2 title_black mb-4 text-center">Ожидание верификации
                        карты</h2>
                </v-row>
                <v-row class="confirm__row">
                    <p class="confirm__text text-center">Внимательно пока проверьте правильность заполненных данных!</p>
                </v-row>
                <v-row class="confirm__row">
                    <v-sheet class="confirm__table-sheet" rounded>
                        <v-table class="confirm__table request-table mb-3">
                            <tbody>
                            <tr>
                                <td class="request-table__item text-right">Направление обмена</td>
                                <td class="request-table__item">
                                    {{ exchangeData.selectedGiveCurrency }} {{ exchangeData.giveTikker }} /
                                    {{ exchangeData.selectedGetCurrency }} {{ exchangeData.getTikker }}
                                </td>
                            </tr>
                            <tr>
                                <td class="request-table__item text-right">Обмен по курсу</td>
                                <td class="request-table__item">
                                    {{ exchangeData.give }} {{ exchangeData.giveTikker }} = {{ exchangeData.get }}
                                    {{ exchangeData.getTikker }}
                                </td>
                            </tr>
                            <tr>
                                <td class="request-table__item text-right">Отправляете</td>
                                <td class="request-table__item">{{ exchangeData.give }} {{ exchangeData.giveTikker }}
                                </td>
                            </tr>
                            <tr>
                                <td class="request-table__item text-right">Получаете</td>
                                <td class="request-table__item">{{ exchangeData.get }} {{ exchangeData.getTikker }}</td>
                            </tr>
                            <tr>
                                <td class="request-table__item text-right">Номер вашей карты</td>
                                <td class="request-table__item">{{ exchangeData.cardNumber }}</td>
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
            </v-container>
        </v-sheet>
    </div>
</template>
<script>
import {defineComponent} from 'vue';
import {mapGetters, mapMutations} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'VerificationView',

    data: () => ({
        exchangeData: null,
    }),
    created() {
        this.exchangeData = this.getExchangeData;
    },
    mounted() {
        this.checkVerification();
    },
    methods: {
        ...mapMutations([
            'setExchangeData',
        ]),
        async checkVerification() {
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);

            let response = await fetch('/api/exchange/await', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                if (response.status === 200) {
                    this.$emit('complete');
                    this.$emit('nextStep');
                }
            } else {
                await this.checkVerification();
            }
        },
    },
    computed: {
        ...mapGetters([
            'getExchangeData',
            'getVerificationFile',
            'getUuid',
        ]),
    }
});
</script>
