<template>
    <v-table class="request-table mb-3">
        <tbody>
        <tr>
            <td class="request-table__item text-right">Направление обмена</td>
            <td class="request-table__item">
                {{ getExchangeData.selectedGiveCurrency }} ({{ getExchangeData.giveTikker }})
                <v-icon class="request-table__item-icon" color="black" icon="mdi-sync"></v-icon>
                {{ getExchangeData.selectedGetCurrency }} ({{ getExchangeData.getTikker }})
            </td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Обмен по курсу</td>
            <td class="request-table__item">
                {{ getExchangeData.give }} {{ getExchangeData.giveTikker }} = {{ getExchangeData.get }}
                {{ getExchangeData.getTikker }}
            </td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Отправляете</td>
            <td class="request-table__item">
                {{ getExchangeData.give }} {{ getExchangeData.giveTikker }}
            </td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Получаете</td>
            <td class="request-table__item">{{ getExchangeData.get }} {{ getExchangeData.getTikker }}</td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Номер вашей карты</td>
            <td class="request-table__item">{{ getExchangeData.cardNumber }}</td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Ваш крипто кошелек</td>
            <td class="request-table__item">{{ getExchangeData.cryptoNumber }}</td>
        </tr>
        <tr>
            <td class="request-table__item text-right">Ваш email</td>
            <td class="request-table__item">{{ getExchangeData.email }}</td>
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
    }),
    methods: {
    },
    computed: {
        ...mapGetters([
            'getExchangeData',
        ]),
    }
});
</script>
