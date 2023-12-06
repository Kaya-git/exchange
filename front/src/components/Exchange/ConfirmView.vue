<template>
  <div class="confirm">
    <v-sheet rounded class="confirm__sheet pa-3 rounded-t-0">
      <v-container fluid class="confirm__container">
        <v-row class="confirm__row">
          <h2 class="confirm__title title title_h2 title_black mb-4 text-center">Подтвердите создание заявки</h2>
        </v-row>
        <v-row class="confirm__row">
          <p class="confirm__text text-center">Внимательно проверьте правильность заполненных данных!</p>
        </v-row>
        <v-row class="confirm__row">
          <v-sheet class="confirm__table-sheet" rounded>
            <v-table class="confirm__table request-table mb-3">
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
        <v-row class="confirm__row mb-8 flex-column align-center">
          <p class="confirm__text text-center mb-4">
            Курс зафиксирован на 10 минут, до отмены подтверждения заявки:
          </p>
          <timer-view :custom-class="'confirm__timer'" :init="600" :route="ExchangeView"></timer-view>
        </v-row>
        <v-row class="confirm__row">
          <v-btn @click="isModalVisible = true" color="success" class="confirm__btn" size="large">Создать заявку</v-btn>
        </v-row>
      </v-container>
    </v-sheet>
  </div>
  <confirm-modal
      :model-value="isModalVisible"
      :msg="'Подтвердите, что введенные данные верны'"
      @confirmed="confirm"
      @canceled="isModalVisible = !isModalVisible">
  </confirm-modal>
  <verification-modal
      :model-value="isVerificationModalVisible"
      :msg="'Загрузите фото для верификации вашей карты'"
      @confirmed="verification"
      @canceled="isVerificationModalVisible = !isVerificationModalVisible"
  ></verification-modal>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import { mapGetters, mapMutations } from 'vuex';
import {prepareData, getCookie} from '@/helpers';

export default defineComponent({
  name: 'ConfirmView',

  data: () => ({
    exchangeData: null,
    error: {
      'status': false,
      'message': '',
    },
    isModalVisible: false,
    isVerificationModalVisible: false,
  }),
  created() {
    this.exchangeData = this.getExchangeData;
  },
  components: {
    TimerView: defineAsyncComponent({
      loader: () => import("../Utils/TimerView"),
    }),
    ConfirmModal: defineAsyncComponent({
      loader: () => import("../Modal/ConfirmModal"),
    }),
    VerificationModal: defineAsyncComponent({
      loader: () => import("../Modal/VerificationModal"),
    }),
  },
  methods: {
    ...mapMutations([
      'setExchangeData',
    ]),
    async confirmRequest() {
      let details = {
        'user_uuid': this.getExchangeData.uuid,
      }

      let formBody = prepareData(details);
      let response = await fetch('/api/exchange/confirm_order/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept':  'application/json',
        },
        body: formBody
      });

      if (!response.ok) {
        this.error.status = true;
        this.error.message = 'Не удалось  отправить запрос:('
      } else {
        let result = await response.json();
        let exchangeData = {};
        exchangeData.name = result.client_cc_holder;
        exchangeData.email = result.client_email;
        exchangeData.cardNumber = result.client_credit_card_number;
        exchangeData.cryptoNumber = result.client_crypto_wallet;
        exchangeData.giveTikker = result.client_sell_currency.tikker;
        exchangeData.give = result.client_sell_value;
        exchangeData.selectedGiveCurrency = result.client_sell_currency.name;
        exchangeData.getTikker = result.client_buy_currency.tikker;
        exchangeData.get = result.client_buy_value;
        exchangeData.selectedGetCurrency = result.client_buy_currency.name;
        exchangeData.uuid = getCookie('user_uuid');

        this.setExchangeData(exchangeData);
      }
    },
    async confirm() {
      let details = {
        'user_uuid': this.getExchangeData.uuid,
      }
      let formBody = prepareData(details);
      let response = await fetch('/api/exchange/confirm_button', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept':  'application/json',
        },
        body: formBody
      });
      if (response.ok) {
        this.isVerificationModalVisible = true;
      }
      this.isModalVisible = false;
    },
    async verification() {
      const formData = new FormData();
      formData.append('user_uuid', this.getExchangeData.uuid);
      formData.append('cc_image', this.getVerificationFile);

      let response = await fetch('/api/exchange/cc_conformation_form', {
        method: 'POST',
        body: formData
      });
      console.log(response);
      // if (response.ok) {
      //
      // }
    }
  },
  computed: {
    ...mapGetters([
      'getExchangeData',
      'getVerificationFile',
    ]),
  }
});
</script>
