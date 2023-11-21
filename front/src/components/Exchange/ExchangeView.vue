<template>
    <div class="exchange">
        <div class="exchange__wrapper">
            <v-container class="exchange-mobile">
                <v-row class="exchange__tabs mb-n7">
                    <v-col class="exchange__tab-col d-flex justify-center" @click="activeTab = 'step1'">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step1" :disabled="activeTab !== 'step1'">Шаг 1</v-btn>
                    </v-col>
                    <v-col class="exchange__tab-col d-flex justify-center" @click="activeTab == 'step3' ? activeTab = 'step2' : false">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step2" :disabled="activeTab !== 'step2'">Шаг 2</v-btn>
                    </v-col>
                    <v-col class="exchange__tab-col d-flex justify-center">
                        <v-btn class="exchange__tab-btn sky-btn" data-tab-id="step3" :disabled="activeTab !== 'step3'">Шаг 3</v-btn>
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
                                    v-for="(currency, i) in currencies.give"
                                    :key="i"
                                    :value="currency"
                                    v-slot="{selectedClass, toggle}">
                                        <v-btn 
                                        class="currency-list__btn currency-btn"
                                        :class="selectedClass"
                                        size="x-large"
                                        @click="toggle">
                                            <template v-slot:prepend>
                                                <span class="currency-btn__img">
                                                    <img :src="currency.src" :alt="currency.name">
                                                </span>
                                            </template>
                                            {{currency.name}}
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
                                        v-for="(currency, i) in currencies.give"
                                        :key="i"
                                        :value="currency"
                                        v-slot="{selectedClass, toggle}">
                                        <v-btn 
                                        class="currency-list__btn currency-btn" 
                                        :class="selectedClass"
                                        size="x-large"
                                        @click="toggle">
                                            <template v-slot:prepend>
                                                <span class="currency-btn__img">
                                                    <img :src="currency.src" :alt="currency.name">
                                                </span>
                                            </template>
                                            {{currency.name}}
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
                                            name="give_currency"
                                            placeholder="1000"
                                            :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="ФИО"
                                            :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Номер карты"
                                            :rules="[rules.required, rules.cardNumberRule]">
                                            </v-text-field>
                                            <h3 class="exchange-data__title title title_h3">
                                                На
                                            </h3>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            :placeholder="randomPlaceholderCrypto()"
                                            :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Крипто кошелек"
                                            :rules="[rules.required]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="email"
                                            placeholder="E-mail"
                                            :rules="[rules.required]">
                                            </v-text-field>
                                            <div class="exchange-data__privacy">
                                                <v-checkbox hide-details required class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Даю согласие с <a href="#">условиями обмена</a>, <a href="#">соглашением</a> и <a href="#">политикой KYC/AML</a></div>
                                                    </template>
                                                </v-checkbox>
                                                <v-checkbox hide-details required class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Согласен с тем, что сумму более ₽300'000 необходимо <a href="#">отправлять частями</a></div>
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
                            v-for="(currency, i) in currencies.give"
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
                                            <img :src="currency.src" :alt="currency.name">
                                        </span>
                                    </template>
                                    {{currency.name}}
                                </v-btn>
                            </v-item>
                        </v-item-group>
                    </v-col>
                    <v-col class="exchange-desktop__col v-col-3">
                        <h3 class="exchange-desktop__title title title_h3">Получаете</h3>
                        <v-item-group 
                        v-model="getCurrency"
                        class="exchange-desktop__list currency-list"
                        selected-class="bg-primary">
                            <v-item
                                v-for="(currency, i) in currencies.get"
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
                                                <img :src="currency.src" :alt="currency.name">
                                            </span>
                                        </template>
                                        {{currency.name}}
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
                                                hide-details 
                                                required 
                                                v-model="formData.privacy"
                                                :error="!formData.privacy"
                                                class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Даю согласие с <a href="#">условиями обмена</a>, <a href="#">соглашением</a> и <a href="#">политикой KYC/AML</a></div>
                                                    </template>
                                                </v-checkbox>
                                                <v-checkbox 
                                                hide-details 
                                                required 
                                                v-model="formData.rules"
                                                :error="!formData.rules"
                                                class="exchange-data__checkbox">
                                                    <template v-slot:label>
                                                        <div>Согласен с тем, что сумму более ₽300'000 необходимо <a href="#">отправлять частями</a></div>
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
                privacy: null,
                rules: null,
                give: null,
                get: null,
                rate: '',
            },
            rules: {
                required: value => !!value || 'Обязательно для заполнения',
                cardNumberRule: v => (v && v.length === 16) || 'Номер карты должен содержать 16 цифр',
            }
        }
    },
    computed: {
    },
    methods: {
        randomPlaceholderCrypto() {
            return Math.random().toFixed(8);
        },
        async submit(event) {
            this.loading = true;

            const results = await event;

            this.loading = false;

            if (results.valid) {
                this.$store.commit('setExchangeData', this.formData);
                this.$router.push({
                    name: 'ConfirmExchange', 
                });
            }
        },
        getCurrencies() {
            this.currencies = {
                give: [
                    {id: 1, name: 'Сбербанк RUB', src: 'icons/banks/sber.svg', rate: '', tikker: 'RUB'}, 
                    {id: 2, name: 'Тинькофф RUB', src: 'icons/banks/tinkoff.svg', rate: '', tikker: 'RUB'}, 
                    {id: 3, name: 'Альфа банк RUB', src: 'icons/banks/alfa-bank.svg', rate: '', tikker: 'RUB'}
                ],
                get: [
                    {id: 4, name: 'Bitcoin BTC', src: 'icons/cryptos/bitcoin-btc-logo.svg', rate: '', tikker: 'BTC'},
                    {id: 5, name: 'Ethereum ETH', src: 'icons/cryptos/ethereum-eth-logo.svg', rate: '', tikker: 'ETH'},
                ],
            }

            this.giveCurrency = this.currencies.give[0];
            this.getCurrency = this.currencies.get[0];
        },
        validateGiveNumberInput() {
            this.formData.give = this.formData.give.replace(/[^0-9.-]/g, '');
            let dotCount = this.formData.give.split('.').length - 1;
            if (dotCount > 1) {
                this.formData.give = this.formData.give.slice(0, this.formData.give.lastIndexOf('.'));
            }
        },
        validateGetNumberInput() {
            this.formData.get = this.formData.get.replace(/[^0-9.-]/g, '');
            let dotCount = this.formData.get.split('.').length - 1;
            if (dotCount > 1) {
                this.formData.get = this.formData.get.slice(0, this.formData.get.lastIndexOf('.'));
            }
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
        }
    },
    created() {
        this.getCurrencies();
    },
    mounted() {
        this.tabs = document.querySelectorAll('[data-tab-id]');
    },
});
</script>