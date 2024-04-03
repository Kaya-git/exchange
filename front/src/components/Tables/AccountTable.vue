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
        <template v-else>
            <tr
                v-for="item in table.tbody"
                :key="item.id"
                class="account-table__body-row">
                <td class="account-table__item">
                    {{item.holder}}
                </td>
                <td class="account-table__item">
                    {{item.number}}
                </td>
                <td class="account-table__item">
                    {{item.is_verified ? 'Верифицировано' : 'Не верифицировано'}}
                </td>
            </tr>
        </template>
        </tbody>
    </v-table>

</template>
<script>
import {defineComponent, reactive} from 'vue';
import {mapGetters} from 'vuex';

export default defineComponent({
    name: 'AccountTable',

    data: () => ({
        table: reactive({
            thead: [
                'Наименование',
                'Номер счета',
                'Статус',
            ],
            tbody: []
        })
    }),
    mounted() {
        this.table.tbody = this.getUserData.verified_po;
    },
    computed: {
        ...mapGetters([
           'getUserData',
            'getUuid'
        ]),
    }
});
</script>
