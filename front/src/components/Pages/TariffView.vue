<template>
    <div class="tariff">
        <v-sheet rounded class="tariff__sheet pa-4">
            <h1 class="tariff__title title title_h1 mb-4">Тарифы</h1>
            <v-container fluid class="tariff__container">
                <v-table class="tariff__table">
                    <thead class="tariff__table-head">
                    <tr class="tariff__table-head-row">
                        <th v-for="(title, i) in tariffs.thead" :key="i">{{title}}</th>
                    </tr>
                    </thead>
                    <tbody class="tariff__table-body">
                    <template
                        v-for="(tariff, i) in tariffs.tbody"
                        :key="i">
                        <template v-if="typeof tariff === 'object'">
                            <tr
                                v-for="bank in banks"
                                :key="bank.name"
                                class="tariff__table-body-row">
                                <td>
                                    <div class="tariff__table-cell">
                                        <img :src="bank.icon" :alt="bank.name">
                                        <span>{{tariff.coin_price}} {{bank.name}} RUB</span>
                                    </div>
                                </td>
                                <td>
                                    <div class="tariff__table-cell">
                                        <img :src="'/' + tariff.icon" alt="">
                                        <span>1 {{tariff.name}} {{tariff.tikker}}</span>
                                    </div>
                                </td>
                                <td>
                                    <div class="tariff__table-cell">
                                        <span>{{tariff.reserve}} {{tariff.name}} {{tariff.tikker}}</span>
                                    </div>
                                </td>
                            </tr>
                        </template>
                        <tr
                            v-else
                            class="tariff__table-body-row">
                            <td colspan="3">
                                {{tariff}}
                            </td>
                        </tr>
                    </template>
                    </tbody>
                </v-table>
            </v-container>
        </v-sheet>
    </div>
</template>

<script>
import {defineComponent, reactive} from 'vue';
import {mapActions} from 'vuex';

export default defineComponent({
    name: 'TariffView',

    data: () => ({
        tariffs: reactive({
            thead: [
                'Отдаете',
                'Получаете',
                'Резерв средств',
            ],
            tbody: [],
        }),
        banks: [
            {
                name: 'Тинькофф',
                icon: '/icons/banks/tinkoff.svg'
            },
            {
                name: 'Сбербанк',
                icon: '/icons/banks/sber.svg'
            }
        ]
    }),
    created() {
        this.getTariffs();
    },
    mounted() {
        this.resizeBg();
    },
    methods: {
        ...mapActions([
            'resizeBg',
        ]),
        async getTariffs() {
            let response = await fetch('/api/currency/tariffs');
            if (response.ok && response.status === 200) {
                let result = await response.json();
                let cryptos = [];
                let tariffs = [];
                result.forEach(item => {
                    if (!cryptos.includes(item.name)) {
                        cryptos.push(item.name);
                        tariffs.push(item.name);
                    }
                    tariffs.push(item);
                });
                this.tariffs.tbody = tariffs;
            }
        }
    }
});
</script>
