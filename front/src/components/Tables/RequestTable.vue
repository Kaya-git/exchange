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
                    <span>{{item.user_sell_sum}}</span>
                    <v-icon color="black" icon="mdi-sync"></v-icon>
                    <span>{{item.user_buy_sum}}</span>
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
import {mapMutations } from 'vuex'

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
      this.getOrders();
    },
    methods: {
        ...mapMutations([
            'setUserOrders',
        ]),
        async getOrders() {
            let response = await fetch('/api/lk/orders');
            if (response.ok && response.status === 200) {
                this.table.tbody = await response.json();
                this.setUserOrders(this.table.tbody);
            }
        }
    }
});
</script>
