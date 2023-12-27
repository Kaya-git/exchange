<template>
    <v-table class="account-table" fixed-header>
        <thead class="account-table__head">
        <tr class="account-table__head-row">
            <th class="account-table__head-item" v-for="(title, i) in table.thead" :key="i">{{title}}</th>
        </tr>
        </thead>
        <tbody class="account-table__body">
        <tr v-if="!table.tbody.length" class="account-table__body-row">
            <td class="account-table__empty" :colspan="table.thead.length"><span>Здесь пока ничего нет</span></td>
        </tr>
        </tbody>
    </v-table>

</template>
<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'AccountTable',

    data: () => ({
        table: {
            thead: [
                'Наименование',
                'Номер счета',
                'Действия',
            ],
            tbody: []
        }
    }),
});
</script>
