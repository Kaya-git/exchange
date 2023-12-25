<template>
    <div class="exchange">
        <div class="exchange__wrapper">
            <v-container class="exchange-mobile">
                <v-row class="exchange__tabs mb-n7">
                    <v-col class="exchange__tab-col d-flex justify-center" @click="activeTab = 'step1'">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step1" :disabled="activeTab !== 'step1'">
                            Шаг 1
                        </v-btn>
                    </v-col>
                    <v-col class="exchange__tab-col d-flex justify-center"
                           @click="activeTab == 'step3' ? activeTab = 'step2' : false">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step2" :disabled="activeTab !== 'step2'">
                            Шаг 2
                        </v-btn>
                    </v-col>
                    <v-col class="exchange__tab-col d-flex justify-center">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step3" :disabled="activeTab !== 'step3'">
                            Шаг 3
                        </v-btn>
                    </v-col>
                </v-row>
                <v-row v-if="activeTab === 'step1'" class="exchange__tab exchange-tab mx-n4">
                    <v-container class="exchange__tab-head">
                        <v-row class="exchange__tab-head-row align-center">
                            <v-col>
                                <h2 class="exchange__tab-title title title_h2">
                                    Отдаете
                                </h2>
                            </v-col>
                            <v-col class="d-flex justify-end">
                                <v-btn color="white" size="large" variant="outlined" @click="activeTab = 'step2'">
                                    Продолжить
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-container class="exchange-tab__content">
                        <v-row class="exchange-tab__content-row">
                            <v-col class="exchange-tab__search col-8">
                                <v-text-field
                                    class="currency-text-field"
                                    placeholder="Найти валюту"
                                    color="white"
                                    bg-color="white"
                                    hide-details="auto"
                                    type="input"
                                    append-inner-icon='mdi-magnify'></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row class="exchange-tab__content-row">
                            <v-container class="exchange-tab__currency-list currency-list">
                                <v-item-group
                                    v-model="giveCurrency"
                                    selected-class="bg-primary"
                                    class="currency-list__group">
                                    <v-item
                                        class="currency-list__item"
                                        v-for="(currency, i) in currenciesApi.banks"
                                        :key="i"
                                        :value="currency"
                                        v-slot="{selectedClass, select}">
                                        <v-btn
                                            class="currency-list__btn currency-btn"
                                            :class="selectedClass"
                                            size="x-large"
                                            @click="select">
                                            <template v-slot:prepend>
                                                <span class="currency-btn__img">
                                                    <img :src="currency.icon" :alt="currency.name">
                                                </span>
                                            </template>
                                            {{ currency.name }}
                                            {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                        </v-btn>
                                    </v-item>
                                </v-item-group>
                            </v-container>
                        </v-row>
                    </v-container>
                </v-row>
                <v-row v-if="activeTab === 'step2'" class="exchange__tab exchange-tab mx-n4">
                    <v-container class="exchange__tab-head">
                        <v-row class="exchange__tab-head-row align-center">
                            <v-col>
                                <h2 class="exchange__tab-title title title_h2">
                                    Получаете
                                </h2>
                            </v-col>
                            <v-col class="d-flex justify-end">
                                <v-btn color="white" size="large" variant="outlined" @click="activeTab = 'step3'">
                                    Продолжить
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-container class="exchange-tab__content">
                        <v-row class="exchange-tab__content-row">
                            <v-col class="exchange-tab__search col-8">
                                <v-text-field
                                    class="currency-text-field"
                                    placeholder="Найти валюту"
                                    color="white"
                                    bg-color="white"
                                    hide-details="auto"
                                    type="input"
                                    append-inner-icon="mdi-magnify"></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row class="exchange-tab__content-row">
                            <v-container class="exchange-tab__currency-list currency-list">
                                <v-item-group
                                    class="currency-list__group"
                                    selected-class="bg-primary"
                                    v-model="getCurrency">
                                    <v-item
                                        class="currency-list__item"
                                        v-for="(currency, i) in currenciesApi.crypto"
                                        :key="i"
                                        :value="currency"
                                        v-slot="{selectedClass, select}">
                                        <v-btn
                                            class="currency-list__btn currency-btn"
                                            :class="selectedClass"
                                            size="x-large"
                                            @click="select">
                                            <template v-slot:prepend>
                                                <span class="currency-btn__img">
                                                    <img :src="currency.icon" :alt="currency.name">
                                                </span>
                                            </template>
                                            {{ currency.name }}
                                            {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                        </v-btn>
                                    </v-item>
                                </v-item-group>
                            </v-container>
                        </v-row>
                    </v-container>
                </v-row>
                <v-row v-if="activeTab === 'step3'" class="exchange__tab exchange-tab mx-n4">
                    <v-container class="exchange__tab-head">
                        <v-row class="exchange__tab-head-row align-center">
                            <h2 class="exchange__tab-title title title_h2">
                                Ваши данные
                            </h2>
                        </v-row>
                    </v-container>
                    <v-container class="exchange-tab__content d-flex justify-center">
                        <div class="exchange-tab__exchange-data exchange-data">
                            <v-container class="exchange-data__wrapper">
                                <v-row>
                                    <v-col>
                                        <v-form validate-on="submit lazy" @submit.prevent="submit">
                                            <h3 class="exchange-data__title title title_h3">
                                                Меняем
                                            </h3>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="1000"
                                                v-model="formData.give"
                                                :rules="[rules.required]"
                                                @input="validateGiveNumberInput"
                                                :suffix="giveCurrency.tikker">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="ФИО"
                                                v-model="formData.name"
                                                :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="Номер карты"
                                                v-model="formData.cardNumber"
                                                :rules="[rules.required, rules.cardNumberRule]"
                                                @input="formatCardNumber">
                                            </v-text-field>
                                            <h3 class="exchange-data__title title title_h3">
                                                На
                                            </h3>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                :placeholder="randomPlaceholderCrypto()"
                                                v-model="formData.get"
                                                :rules="[rules.required]"
                                                @input="validateGetNumberInput"
                                                :suffix="getCurrency.tikker">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="Крипто кошелек"
                                                v-model="formData.cryptoNumber"
                                                :rules="[rules.required, validateCryptoWallet]">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="email"
                                                placeholder="E-mail"
                                                v-model="formData.email"
                                                :rules="[rules.required]">
                                            </v-text-field>
                                            <div class="exchange-data__privacy">
                                                <v-checkbox
                                                    v-model="formData.privacy.value"
                                                    :error="formData.privacy.error && !formData.privacy.value"
                                                    :rules="[rules.required]"
                                                    class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Даю согласие с <a href="#">условиями обмена</a>, <a
                                                            href="#">соглашением</a> и <a href="#">политикой KYC/AML</a>
                                                        </div>
                                                    </template>
                                                </v-checkbox>
                                                <v-checkbox
                                                        v-model="formData.rules.value"
                                                        :error="formData.rules.error && !formData.rules.value"
                                                        :rules="[rules.required]"
                                                        class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Согласен с тем, что сумму более ₽300'000 необходимо <a
                                                            href="#">отправлять частями</a></div>
                                                    </template>
                                                </v-checkbox>
                                            </div>
                                            <div class="exchange-data__submit">
                                                <v-btn type="submit" size="large">Перейти к оплате</v-btn>
                                            </div>
                                        </v-form>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </div>
                    </v-container>
                </v-row>
            </v-container>
            <v-container class='exchange-desktop'>
                <v-row class="exchange-desktop__content">
                    <v-col class="exchange-desktop__col v-col-3">
                        <h3 class="exchange-desktop__title title title_h3">Отдаете</h3>
                        <v-item-group
                            v-model="giveCurrency"
                            selected-class="bg-primary"
                            class="exchange-desktop__list currency-list">
                            <v-item
                                v-for="(currency, i) in currenciesApi.banks"
                                :key="i"
                                :value="currency"
                                v-slot="{selectedClass,select}">
                                <v-btn
                                    class="currency-list__btn currency-btn"
                                    @click="select"
                                    :class="selectedClass"
                                    size="x-large">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img :src="currency.icon" :alt="currency.name">
                                        </span>
                                    </template>
                                    {{ currency.name }} {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                </v-btn>
                            </v-item>
                            <v-item
                                v-for="(currency, i) in currenciesApi.crypto"
                                :key="i"
                                :value="currency"
                                v-slot="{selectedClass,select}">
                                <v-btn
                                    class="currency-list__btn currency-btn"
                                    @click="select"
                                    :class="selectedClass"
                                    size="x-large">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img :src="currency.icon" :alt="currency.name">
                                        </span>
                                    </template>
                                    {{ currency.name }} {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                </v-btn>
                            </v-item>
                        </v-item-group>
                    </v-col>
                    <v-col class="exchange-desktop__col v-col-3">
                        <h3 class="exchange-desktop__title title title_h3">Получаете</h3>
                        <v-item-group
                            v-model="getCurrency"
                            v-if="giveCurrency && giveCurrency.type === 'fiat'"
                            class="exchange-desktop__list currency-list"
                            selected-class="bg-primary">
                            <v-item
                                v-for="(currency, i) in currenciesApi.crypto"
                                :key="i"
                                :value="currency"
                                v-slot="{selectedClass,select}">
                                <v-btn
                                    class="currency-list__btn currency-btn"
                                    :class="selectedClass"
                                    size="x-large"
                                    @click="select">
                                    <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img :src="currency.icon" :alt="currency.name">
                                            </span>
                                    </template>
                                    {{ currency.name }} {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                </v-btn>
                            </v-item>
                        </v-item-group>
                        <v-item-group
                            v-model="getCurrency"
                            v-if="giveCurrency && giveCurrency.type === 'crypto'"
                            class="exchange-desktop__list currency-list"
                            selected-class="bg-primary">
                            <v-item
                                v-for="(currency, i) in currenciesApi.banks"
                                :key="i"
                                :value="currency"
                                v-slot="{selectedClass,select}">
                                <v-btn
                                    class="currency-list__btn currency-btn"
                                    :class="selectedClass"
                                    size="x-large"
                                    @click="select">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img :src="currency.icon" :alt="currency.name">
                                        </span>
                                    </template>
                                    {{ currency.name }} {{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }}
                                </v-btn>
                            </v-item>
                        </v-item-group>
                    </v-col>
                    <v-col class="exchange-desktop__col v-col-6">
                        <h3 class="exchange-desktop__title title title_h3">Обмен</h3>
                        <div class="exchange-desktop__trade exchange-data">
                            <v-container class="exchange-data__wrapper">
                                <v-row>
                                    <v-col>
                                        <v-form
                                            validate-on="submit lazy" @submit.prevent="submit">
                                            <h3 class="exchange-data__title title title_h3">
                                                Меняем
                                            </h3>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="1000"
                                                v-model="formData.give"
                                                :rules="[rules.required]"
                                                @input="validateGiveNumberInput"
                                                :suffix="giveCurrency ? (giveCurrency.type === 'fiat' ? 'RUB' : giveCurrency.tikker) : ''">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="ФИО"
                                                v-model="formData.name"
                                                :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="Номер карты"
                                                v-model="formData.cardNumber"
                                                :rules="[rules.required, rules.cardNumberRule]"
                                                @input="formatCardNumber">
                                            </v-text-field>
                                            <h3 class="exchange-data__title title title_h3">
                                                На
                                            </h3>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                :placeholder="randomPlaceholderCrypto()"
                                                v-model="formData.get"
                                                :rules="[rules.required]"
                                                @input="validateGetNumberInput"
                                                :suffix="getCurrency ? (getCurrency.type === 'fiat' ? 'RUB' : getCurrency.tikker) : ''">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="text"
                                                placeholder="Крипто кошелек"
                                                v-model="formData.cryptoNumber"
                                                :rules="[rules.required, validateCryptoWallet]">
                                            </v-text-field>
                                            <v-text-field
                                                class="exchange-data__text-field"
                                                type="email"
                                                placeholder="E-mail"
                                                v-model="formData.email"
                                                :rules="[rules.required]">
                                            </v-text-field>
                                            <div class="exchange-data__privacy">
                                                <v-checkbox
                                                    hide-details
                                                    v-model="formData.privacy.value"
                                                    :error="formData.privacy.error && !formData.privacy.value"
                                                    class="exchange-data__checkbox"
                                                    :rules="[rules.required]">
                                                    <template v-slot:label>
                                                        <div>Даю согласие с <a href="#">условиями обмена</a>, <a
                                                            href="#">соглашением</a> и <a href="#">политикой KYC/AML</a>
                                                        </div>
                                                    </template>
                                                </v-checkbox>
                                                <v-checkbox
                                                    hide-details
                                                    v-model="formData.rules.value"
                                                    :error="formData.rules.error && !formData.rules.value"
                                                    :rules="[rules.required]"
                                                    class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Согласен с тем, что сумму более ₽300'000 необходимо <a
                                                            href="#">отправлять частями</a></div>
                                                    </template>
                                                </v-checkbox>
                                            </div>
                                            <div class="exchange-data__submit">
                                                <v-btn type="submit" size="large">Перейти к оплате</v-btn>
                                            </div>
                                        </v-form>
                                    </v-col>
                                </v-row>
                            </v-container>
                        </div>
                    </v-col>
                </v-row>
            </v-container>
        </div>
    </div>
</template>

<script>
import {defineComponent} from 'vue';
import {mapMutations, mapGetters} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'ExchangeView',
    data() {
        return {
            tabs: [],
            activeTab: 'step1',
            loading: false,
            timeout: null,
            currencies: null,
            giveCurrency: null,
            getCurrency: null,
            formData: {
                name: '',
                email: '',
                cardNumber: '',
                cryptoNumber: '',
                privacy: {
                    value: false,
                    error: false,
                },
                rules: {
                    value: false,
                    error: false,
                },
                give: null,
                get: null,
                giveTikker: '',
                getTikker: '',
                selectedGiveCurrency: '',
                selectedGetCurrency: '',
                exchangeRate: null,
            },
            currenciesApi: {
                banks: [],
                crypto: [],
            },
            rules: {
                required: value => !!value || 'Обязательно для заполнения',
                cardNumberRule: v => (v && v.length === 19) || 'Номер карты должен содержать 16 цифр',
            }
        }
    },
    computed: {
        ...mapGetters([
           'getUuid'
        ]),
    },
    watch: {
        getCurrency(newCur) {
            this.getExchangeRate(this.giveCurrency.tikker, newCur.tikker).then(result => {
                this.formData.exchangeRate = result;
                this.recalculate();
            });
        },
        giveCurrency(newCur) {
            if (newCur.type === 'crypto') {
                this.getCurrency = this.currenciesApi['banks'][0];
            }
            if (newCur.type === 'fiat') {
                this.getCurrency = this.currenciesApi['crypto'][0];
            }
        }
    },
    methods: {
        ...mapMutations([
            'setExchangeData',
        ]),
        recalculate() {
            let get = null;
            if (this.formData.exchangeRate && this.formData.give && this.formData.get) {
                if (this.giveCurrency.type === 'crypto') {
                    get = (this.formData.give * this.formData.exchangeRate).toFixed(2);
                } else {
                    get = (this.formData.give / this.formData.exchangeRate).toFixed(8);
                }
            }
            this.formData.get = get;
        },
        randomPlaceholderCrypto() {
            return Math.random().toFixed(8);
        },
        async submit(event) {
            this.loading = true;

            const results = await event;

            this.loading = false;

            if (results.valid) {
                this.formData.giveTikker = this.giveCurrency.tikker;
                this.formData.getTikker = this.getCurrency.tikker;
                this.formData.selectedGetCurrency = this.getCurrency.name;
                this.formData.selectedGiveCurrency = this.giveCurrency.name;
                this.setExchangeData(this.formData);
                let isDataSended = await this.sendData();
                if (isDataSended) {
                    this.$router.push({
                        name: 'ExchangeSteps',
                    });
                }
            } else {
                this.formData.rules.error = !this.formData.rules.value;
                this.formData.privacy.error = !this.formData.privacy.value;
            }
        },
        async sendData() {
            let details = {
                'client_sell_value': this.formData.give,
                'client_sell_tikker': this.giveCurrency.tikker,
                'client_buy_value': this.formData.get,
                'client_buy_tikker': this.getCurrency.tikker,
                'client_email': this.formData.email,
                'client_crypto_wallet': this.formData.cryptoNumber,
                'client_credit_card_number': this.formData.cardNumber,
                'client_cc_holder': this.formData.name,
                'user_uuid': this.getUuid,
            };


            let formBody = prepareData(details);

            let response = await fetch('/api/exchange/exchange_form', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                return await response.json();
            }
            return false;

        },
        validateGiveNumberInput() {
            this.formData.give = this.formData.give.replace(/[^0-9.-]/g, '');
            let dotCount = this.formData.give.split('.').length - 1;
            if (dotCount > 1) {
                this.formData.give = this.formData.give.slice(0, this.formData.give.lastIndexOf('.'));
            }
            let amount = null;
            if (this.formData.exchangeRate && this.formData.give) {
                if (this.giveCurrency.type === 'crypto') {
                    amount = (this.formData.give * this.formData.exchangeRate).toFixed(2);
                } else {
                    amount = (this.formData.give / this.formData.exchangeRate).toFixed(8);
                }
            }
            this.formData.get = amount;
        },
        validateGetNumberInput() {
            this.formData.get = this.formData.get.replace(/[^0-9.-]/g, '');
            let dotCount = this.formData.get.split('.').length - 1;
            if (dotCount > 1) {
                this.formData.get = this.formData.get.slice(0, this.formData.get.lastIndexOf('.'));
            }
            let amount = null;
            if (this.formData.exchangeRate && this.formData.get) {
                if (this.giveCurrency.type === 'fiat') {
                    amount = (this.formData.get / this.formData.exchangeRate).toFixed(8);
                } else {
                    amount = (this.formData.get * this.formData.exchangeRate).toFixed(2);
                }
            }
            this.formData.give = amount;
        },
        formatCardNumber() {
            // Удаляем все нецифровые символы из введенного значения
            let formattedInput = this.formData.cardNumber.replace(/\D/g, '');
            // Добавляем пробелы после каждых 4 цифр
            if (formattedInput.length > 0) {
                formattedInput = formattedInput.match(new RegExp('.{1,4}', 'g')).join(' ');
            }
            if (this.formData.cardNumber.length > 19) {
                formattedInput = formattedInput.slice(0, 19);
            }
            this.formData.cardNumber = formattedInput;
        },
        validateCryptoWallet() {
            let regex = /^(1|3|bc1q|bc1p)[A-Za-z0-9]{22,40}$/;
            if (regex.test(this.formData.cryptoNumber)) {
                return true;
            }

            regex = /^(L|3|M|ltc1)[A-Za-z0-9]{21,45}$/;
            if (regex.test(this.formData.cryptoNumber)) {
                return true;
            }

            regex = /^0x[A-Fa-f0-9]{38,42}$/;
            if (regex.test(this.formData.cryptoNumber)) {
                return true;
            }

            regex = /^T[A-Za-z0-9]{31,32}$/;
            if (regex.test(this.formData.cryptoNumber)) {
                return true;
            }

            regex = /^0x[A-Fa-f0-9]{39,40}$/;
            if (regex.test(this.formData.cryptoNumber)) {
                return true;
            }

            return 'Невалидный номер кошелька';
        },
        async getApiCurriencies() {
            let response = await fetch('/api/currency/list');
            let data = await response.json();
            if (!data) {
                return false;
            }
            if (!Array.isArray(data)) {
                return false;
            }
            data.forEach(item => {
                if (item.type === 'fiat') {
                    this.currenciesApi.banks.push(item);
                } else {
                    this.currenciesApi.crypto.push(item);
                }
            });
            this.giveCurrency = this.currenciesApi.banks[0];
            this.getCurrency = this.currenciesApi.crypto[0];
            return response;
        },
        async getExchangeRate(giveTikker, getTikker) {
            let response = await fetch('/api/exchange/' + giveTikker + '/' + getTikker);
            let result = await response.json();

            return result['exchange_rate'] ?? null;
        },
    },
    created() {
        this.getApiCurriencies();
    },
    mounted() {
        this.tabs = document.querySelectorAll('[data-tab-id]');
    },
});
</script>