<template>
    <v-table class="request-table">
        <thead class="request-table__head">
        <tr class="request-table__head-row">
            <th class="request-table__head-item" v-for="(title, i) in table.thead" :key="i">{{title}}</th>
        </tr>
        </thead>
        <tbody class="request-table__body">
        <tr v-if="!table.tbody.length" class="request-table__body-row">
            <td class="request-table__empty" :colspan="table.thead.length"><span>Здесь пока ничего нет</span></td>
        </tr>
        <template v-else>
            <tr
                v-for="item in table.tbody"
                :key="item.id"
                class="request-table__body-row">
                <td class="request-table__item">
                    #{{item.id}}
                </td>
                <td class="request-table__item">
                    <span class="request-table__item-sum">{{item.user_sell_sum}} {{item.sell_currency_tikker}}</span>
                    <v-icon class="request-table__item-icon" color="black" icon="mdi-sync"></v-icon>
                    <span class="request-table__item-sum">{{item.user_buy_sum}} {{item.buy_currency_tikker}}</span>
                </td>
                <td class="request-table__item">
                    {{item.status}}
                </td>
            </tr>
        </template>
        </tbody>
    </v-table>
</template>


<script>
import {defineComponent} from 'vue';
import {mapMutations, mapActions, mapState} from 'vuex'

export default defineComponent({
    name: 'RequestTable',

    data: () => ({
        table: {
            thead: [
                'Номер заявки',
                'Обмен',
                'Статус заявки',
            ],
            tbody: []
        }
    }),
    created() {
      this.getCurrencies().then(() => {
        this.getOrders();
      });
    },
    methods: {
        ...mapMutations([
            'setUserOrders',
        ]),
        ...mapActions([
           'getCurrencies'
        ]),
        async getOrders() {
            let response = await fetch('/api/lk/orders');
            if (response.ok && response.status === 200) {
                this.table.tbody = await response.json();
                this.table.tbody.forEach(order => {
                  let neededBuyCur = this.currencies.find(currency => {
                    return currency.id === order.buy_currency_id;
                  });
                  let neededSellCur = this.currencies.find(currency => {
                    return currency.id === order.sell_currency_id;
                  });
                  order['buy_currency_tikker'] = neededBuyCur.tikker ?? '';
                  order['sell_currency_tikker'] = neededSellCur.tikker ?? '';
                });
                this.setUserOrders(this.table.tbody);
            }
        }
    },
    computed: {
        ...mapState([
           'currencies',
        ]),
    }
});
</script>
