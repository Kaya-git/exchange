<template>
    <v-table class="request-table mb-3">
        <tbody>
        <tr>
            <td class="request-table__item text-right">Направление обмена</td>
            <td class="request-table__item">
                {{ exchangeData.selectedGiveCurrency }} ({{ exchangeData.giveTikker }})
                <v-icon class="request-table__item-icon" color="black" icon="mdi-sync"></v-icon>
                {{ exchangeData.selectedGetCurrency }} ({{ exchangeData.getTikker }})
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
            <td class="request-table__item">
                {{ exchangeData.give }} {{ exchangeData.giveTikker }}
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
</template>


<script>
import {defineComponent} from 'vue';
import {mapGetters} from 'vuex'

export default defineComponent({
    name: 'CurExchangeTable',

    data: () => ({
        exchangeData: null,
    }),
    created() {
        this.exchangeData = this.getExchangeData;
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
