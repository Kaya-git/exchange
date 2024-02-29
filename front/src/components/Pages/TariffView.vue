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
                        v-for="(bank, i) in tariffs.tbody"
                        :key="i">
                        <tr class="tariff__table-body-row">
                            <td colspan="3">
                              {{bank.name}}
                            </td>
                        </tr>
                        <tr
                            v-for="crypto in bank.items"
                            :key="crypto.tikker"
                            class="tariff__table-body-row">
                            <td>
                                <div class="tariff__table-cell">
                                    <img :src="'/' + bank.icon" :alt="bank.name">
                                    <span>{{ crypto.coin_price }} {{ bank.name }} RUB</span>
                                </div>
                            </td>
                            <td>
                                <div class="tariff__table-cell">
                                    <img :src="'/' + crypto.icon" :alt="crypto.name">
                                    <span>1 {{ crypto.name }} {{ crypto.tikker }}</span>
                                </div>
                            </td>
                            <td>
                                <div class="tariff__table-cell">
                                    <span>{{ crypto.reserve }} {{ crypto.name }} {{ crypto.tikker }}</span>
                                </div>
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
import {mapActions, mapState} from 'vuex';

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
    }),
    created() {
        this.getCurrencies().then(() => {
            this.getTariffs();
        });
    },
    methods: {
        ...mapActions([
          'getCurrencies'
        ]),
        async getTariffs() {
            let response = await fetch('/api/currency/tariffs');
            if (response.ok && response.status === 200) {
                let result = await response.json();
                this.findBanks(result);
                this.tariffs.tbody.forEach((bank, i) => {
                    if (result[bank.tikker]) {
                      this.tariffs.tbody[i]['items'] = result[bank.tikker];
                    }
                });
            }
        },
        findBanks(data) {
            for (let tikker in data) {
                let bankCur = this.currencies.find(currency => {
                  return currency.tikker === tikker;
                });
                bankCur['items'] = {};
                this.tariffs.tbody.push(bankCur);
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
