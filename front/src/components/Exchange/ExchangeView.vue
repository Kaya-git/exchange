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
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/sber.svg" alt="">
                                            </span>
                                        </template>
                                        Сбербанк RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/tinkoff.svg" alt="">
                                            </span>
                                        </template>
                                        Тинькофф RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/alfa-bank.svg" alt="">
                                            </span>
                                        </template>
                                        Альфа банк RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/alfa-bank.svg" alt="">
                                            </span>
                                        </template>
                                        Альфа банк RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/alfa-bank.svg" alt="">
                                            </span>
                                        </template>
                                        Альфа банк RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/alfa-bank.svg" alt="">
                                            </span>
                                        </template>
                                        Альфа банк RUB
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/alfa-bank.svg" alt="">
                                            </span>
                                        </template>
                                        Альфа банк RUB
                                    </v-btn>
                                </div>
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
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/cryptos/bitcoin-btc-logo.svg" alt="">
                                            </span>
                                        </template>
                                        Bitcoin BTC
                                    </v-btn>
                                </div>
                                <div class="currency-list__item">
                                    <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/cryptos/ethereum-eth-logo.svg" alt="">
                                            </span>
                                        </template>
                                        Ethereum ETH
                                    </v-btn>
                                </div>
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
                                        <v-form v-model="valid">
                                            <h3 class="exchange-data__title title title_h3">
                                                Меняем
                                            </h3>
                                            <v-text-field 
                                            class="exchange-data__text-field"
                                            type="text"
                                            name="give_currency"
                                            placeholder="1000"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="ФИО"
                                            :rules="rules.nameRules">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Номер карты"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <h3 class="exchange-data__title title title_h3">
                                                На
                                            </h3>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            :placeholder="randomPlaceholderCrypto()"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Крипто кошелек"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="email"
                                            placeholder="E-mail"
                                            :rules="[validateField]">
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
                        <ul class="exchange-desktop__list currency-list">
                            <li class="currency-list__item">
                                <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/banks/sber.svg" alt="">
                                            </span>
                                        </template>
                                        Сбербанк RUB
                                    </v-btn>
                            </li>
                            <li class="currency-list__item">
                                <v-btn class="currency-list__btn currency-btn" size="x-large">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img src="icons/banks/tinkoff.svg" alt="">
                                        </span>
                                    </template>
                                    Тинькофф RUB
                                </v-btn>
                            </li>
                            <li class="currency-list__item">
                                <v-btn class="currency-list__btn currency-btn" size="x-large">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img src="icons/banks/alfa-bank.svg" alt="">
                                        </span>
                                    </template>
                                    Альфа банк RUB
                                </v-btn>
                            </li>
                        </ul>
                    </v-col>
                    <v-col class="exchange-desktop__col v-col-3">
                        <h3 class="exchange-desktop__title title title_h3">Получаете</h3>
                        <ul class="exchange-desktop__list currency-list">
                            <li class="currency-list__item">
                                <v-btn class="currency-list__btn  currency-btn" size="x-large">
                                    <template v-slot:prepend>
                                        <span class="currency-btn__img">
                                            <img src="icons/cryptos/bitcoin-btc-logo.svg" alt="">
                                        </span>
                                    </template>
                                    Bitcoin BTC
                                </v-btn>
                            </li>
                            <li class="currency-list__item">
                                <v-btn class="currency-list__btn currency-btn" size="x-large">
                                        <template v-slot:prepend>
                                            <span class="currency-btn__img">
                                                <img src="icons/cryptos/ethereum-eth-logo.svg" alt="">
                                            </span>
                                        </template>
                                        Ethereum ETH
                                    </v-btn>
                            </li>
                        </ul>
                    </v-col>
                    <v-col class="exchange-desktop__col v-col-6">
                        <h3 class="exchange-desktop__title title title_h3">Обмен</h3>
                        <div class="exchange-desktop__trade exchange-data">
                            <v-container class="exchange-data__wrapper">
                                <v-row>
                                    <v-col>
                                        <v-form v-model="valid">
                                            <h3 class="exchange-data__title title title_h3">
                                                Меняем
                                            </h3>
                                            <v-text-field 
                                            class="exchange-data__text-field"
                                            type="text"
                                            name="give_currency"
                                            placeholder="1000"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="ФИО"
                                            :rules="rules.nameRules">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Номер карты"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <h3 class="exchange-data__title title title_h3">
                                                На
                                            </h3>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            :placeholder="randomPlaceholderCrypto()"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="text"
                                            placeholder="Крипто кошелек"
                                            :rules="[validateField]">
                                            </v-text-field>
                                            <v-text-field
                                            class="exchange-data__text-field"
                                            type="email"
                                            placeholder="E-mail"
                                            :rules="[validateField]">
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
            previousTab: '',
            valid: false,
            formData: {
                name: '',
                email: '',
                cardNumber: '',
                cryptoNumber: '',
                give: 0,
                get: 0,
            },
            rules: {
                nameRules: [
                    value => {
                    if (value) return true

                    return 'Обязательное поле.'
                    },
                    value => {
                    if (value?.length <= 10) return true

                    return 'Name must be less than 10 characters.'
                    },
                ],
            }
        }
    },
    computed: {
    },
    methods: {
        validateField(v) {
            if (!v) {
                return 'Обязательно для заполнения';
            }

            return true;
        },
        randomPlaceholderCrypto() {
            return Math.random().toFixed(8);
        },
    },
    mounted() {
        this.tabs = document.querySelectorAll('[data-tab-id]');
    },
});
</script>