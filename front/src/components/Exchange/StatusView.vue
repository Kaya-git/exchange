<template>
  <div class="status">
    <v-sheet rounded class="status__sheet pa-3 rounded-t-0">
      <v-container fluid class="status__container">
        <v-row class="status__row">
          <h2 class="status__title title title_h2 title_black mb-4 text-center">Подтвердите создание заявки</h2>
        </v-row>
        <v-row class="status__row">
          <p class="status__text text-center">Внимательно проверьте правильность заполненных данных!</p>
        </v-row>
        <v-row class="status__row">
          <v-sheet class="status__table-sheet" rounded>
            <v-table class="status__table request-table mb-3">
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

        </v-row>
      </v-container>
    </v-sheet>
  </div>
</template>
<script>
import {defineComponent} from 'vue';
import { mapGetters, mapMutations } from 'vuex';

export default defineComponent({
  name: 'StatusView',

  data: () => ({
    exchangeData: null,
  }),
  created() {
    this.exchangeData = this.getExchangeData;
  },
  components: {

  },
  methods: {
    ...mapMutations([
      'setExchangeData',
    ]),
  },
  computed: {
    ...mapGetters([
      'getExchangeData',
      'getVerificationFile',
    ]),
  }
});
</script>
