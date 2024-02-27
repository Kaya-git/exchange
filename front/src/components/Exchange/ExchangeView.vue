
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
                    <v-col class="exchange__tab-col d-flex justify-center" @click="activeTab === 'step3' ? activeTab = 'step2' : false">
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
                            <v-col class="v-col-6">
                                <h2 class="exchange__tab-title title title_h2">
                                    Отдаете
                                </h2>
                            </v-col>
                            <v-col class="v-col-6 d-flex justify-end">
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
                                    v-model="search.give"
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
                                        v-for="(currency, i) in filteredGiveBanks"
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
                                            {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
                                        </v-btn>
                                    </v-item>
                                    <v-item
                                        v-for="(currency, i) in filteredGiveCryptos"
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
                                            {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
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
                            <v-col class="v-col-6">
                                <h2 class="exchange__tab-title title title_h2">
                                    Получаете
                                </h2>
                            </v-col>
                            <v-col class="v-col-6 d-flex justify-end">
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
                                    v-model="search.get"
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
                                    v-model="getCurrency"
                                    v-if="giveCurrency && giveCurrency.type === 'fiat'"
                                    class="currency-list__group"
                                    selected-class="bg-primary">
                                    <v-item
                                        v-for="(currency, i) in filteredGetCryptos"
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
                                            {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
                                        </v-btn>
                                    </v-item>
                                </v-item-group>
                                <v-item-group
                                    v-model="getCurrency"
                                    v-if="giveCurrency && giveCurrency.type === 'crypto'"
                                    class="currency-list__group"
                                    selected-class="bg-primary">
                                    <v-item
                                        v-for="(currency, i) in filteredGetBanks"
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
                                            {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
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
                            <v-col>
                                <h2 class="exchange__tab-title title title_h2">
                                    Ваши данные
                                </h2>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-container class="exchange-tab__content d-flex justify-center">
                        <div class="exchange-tab__exchange-data exchange-data">
                            <v-container class="exchange-data__wrapper">
                                <v-row>
                                    <v-col>
                                        <v-form validate-on="submit lazy" @submit.prevent="submit">
                                            <template v-if="!changeForm">
                                                <h3 class="exchange-data__title title title_h3">
                                                    Отдаю
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
                                                    placeholder="Ваш номер карты"
                                                    v-model="formData.cardNumber"
                                                    :rules="[rules.required, rules.cardNumberRule]"
                                                    @input="formatCardNumber">
                                                </v-text-field>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Получаю
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
                                                    :placeholder="'Ваш ' + getCurrencyName + ' кошелек'"
                                                    v-model="formData.cryptoNumber"
                                                    :rules="[rules.required, validateCryptoWallet]">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="email"
                                                    placeholder="E-mail"
                                                    v-model="formData.email"
                                                    :rules="rules.emailRules">
                                                </v-text-field>
                                                <div class="exchange-data__privacy">
                                                    <v-checkbox
                                                        hide-details
                                                        v-model="formData.privacy.value"
                                                        :error="formData.privacy.error && !formData.privacy.value"
                                                        :rules="[rules.required]"
                                                        class="exchange-data__checkbox">
                                                        <template v-slot:label>
                                                            <div>Даю согласие с <RouterLink to="/privacy/">условиями обмена</RouterLink>, <RouterLink
                                                                to="/privacy/">соглашением</RouterLink> и <RouterLink to="/privacy/">политикой KYC/AML</RouterLink>
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
                                                            <div>Согласен с тем, что сумму более ₽300'000 необходимо <RouterLink
                                                                to="/privacy/">отправлять частями</RouterLink></div>
                                                        </template>
                                                    </v-checkbox>
                                                </div>
                                            </template>
                                            <template v-else>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Отдаю
                                                </h3>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    :placeholder="randomPlaceholderCrypto()"
                                                    v-model="formData.give"
                                                    :rules="[rules.required]"
                                                    @input="validateGiveNumberInput"
                                                    :suffix="giveCurrency ? (giveCurrency.type === 'fiat' ? 'RUB' : giveCurrency.tikker) : ''">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    :placeholder="'Ваш ' + giveCurrencyName + ' кошелек'"
                                                    v-model="formData.cryptoNumber"
                                                    :rules="[rules.required, validateCryptoWallet]">
                                                </v-text-field>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Получаю
                                                </h3>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="1000"
                                                    v-model="formData.get"
                                                    :rules="[rules.required]"
                                                    @input="validateGetNumberInput"
                                                    :suffix="getCurrency ? (getCurrency.type === 'fiat' ? 'RUB' : getCurrency.tikker) : ''">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="email"
                                                    placeholder="E-mail"
                                                    v-model="formData.email"
                                                    :rules="rules.emailRules">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="Ваш номер карты"
                                                    v-model="formData.cardNumber"
                                                    :rules="[rules.required, rules.cardNumberRule]"
                                                    @input="formatCardNumber">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="ФИО"
                                                    v-model="formData.name"
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
                                                            <div>Даю согласие с <RouterLink to="/privacy/">условиями обмена</RouterLink>, <RouterLink
                                                                to="/privacy/">соглашением</RouterLink> и <RouterLink to="/privacy/">политикой KYC/AML</RouterLink>
                                                            </div>
                                                        </template>
                                                    </v-checkbox>
                                                </div>
                                            </template>
                                            <div class="exchange-data__submit">
                                                <v-btn
                                                    type="submit"
                                                    size="large"
                                                    :loading="loading"
                                                    :disabled="loading">
                                                    Перейти к оплате
                                                </v-btn>
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
                            <h3 class="currency-list__title title title_h4">Интернет-банкинг</h3>
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
                                    {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
                                </v-btn>
                            </v-item>
                            <h3 class="currency-list__title title title_h4">Криптовалюта</h3>
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
                                    {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
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
                            <h3 class="currency-list__title title title_h4">Криптовалюта</h3>
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
                                    {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
                                </v-btn>
                            </v-item>
                        </v-item-group>
                        <v-item-group
                            v-model="getCurrency"
                            v-if="giveCurrency && giveCurrency.type === 'crypto'"
                            class="exchange-desktop__list currency-list"
                            selected-class="bg-primary">
                            <h3 class="currency-list__title title title_h4">Интернет-банкинг</h3>
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
                                    {{ currency.name }} ({{ currency.coingecko_tik === 'rub' ? 'RUB' : currency.tikker }})
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
                                            <template v-if="!changeForm">
                                                <h3 class="exchange-data__title title title_h3">
                                                    Отдаю
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
                                                    placeholder="Ваш номер карты"
                                                    v-model="formData.cardNumber"
                                                    :rules="[rules.required, rules.cardNumberRule]"
                                                    @input="formatCardNumber">
                                                </v-text-field>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Получаю
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
                                                    :placeholder="'Ваш ' + getCurrencyName + ' кошелек'"
                                                    v-model="formData.cryptoNumber"
                                                    :rules="[rules.required, validateCryptoWallet]">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="email"
                                                    placeholder="E-mail"
                                                    v-model="formData.email"
                                                    :rules="rules.emailRules">
                                                </v-text-field>
                                                <div class="exchange-data__privacy">
                                                    <v-checkbox
                                                        hide-details
                                                        v-model="formData.privacy.value"
                                                        :error="formData.privacy.error && !formData.privacy.value"
                                                        class="exchange-data__checkbox"
                                                        :rules="[rules.required]">
                                                        <template v-slot:label>
                                                            <div>Даю согласие с <RouterLink to="/privacy/">условиями обмена</RouterLink>, <RouterLink
                                                                to="/privacy/">соглашением</RouterLink> и <RouterLink to="/privacy/">политикой KYC/AML</RouterLink>
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
                                                            <div>Согласен с тем, что сумму более ₽300'000 необходимо <RouterLink
                                                                to="/privacy/">отправлять частями</RouterLink></div>
                                                        </template>
                                                    </v-checkbox>
                                                </div>
                                            </template>
                                            <template v-else>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Отдаю
                                                </h3>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    :placeholder="randomPlaceholderCrypto()"
                                                    v-model="formData.give"
                                                    :rules="[rules.required]"
                                                    @input="validateGiveNumberInput"
                                                    :suffix="giveCurrency ? (giveCurrency.type === 'fiat' ? 'RUB' : giveCurrency.tikker) : ''">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    :placeholder="'Ваш ' + giveCurrencyName + ' кошелек'"
                                                    v-model="formData.cryptoNumber"
                                                    :rules="[rules.required, validateCryptoWallet]">
                                                </v-text-field>
                                                <h3 class="exchange-data__title title title_h3">
                                                    Получаю
                                                </h3>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="1000"
                                                    v-model="formData.get"
                                                    :rules="[rules.required]"
                                                    @input="validateGetNumberInput"
                                                    :suffix="getCurrency ? (getCurrency.type === 'fiat' ? 'RUB' : getCurrency.tikker) : ''">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="email"
                                                    placeholder="E-mail"
                                                    v-model="formData.email"
                                                    :rules="rules.emailRules">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="Ваш номер карты"
                                                    v-model="formData.cardNumber"
                                                    :rules="[rules.required, rules.cardNumberRule]"
                                                    @input="formatCardNumber">
                                                </v-text-field>
                                                <v-text-field
                                                    class="exchange-data__text-field"
                                                    type="text"
                                                    placeholder="ФИО"
                                                    v-model="formData.name"
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
                                                            <div>Даю согласие с <RouterLink to="/privacy/">условиями обмена</RouterLink>, <RouterLink
                                                                to="/privacy/">соглашением</RouterLink> и <RouterLink to="/privacy/">политикой KYC/AML</RouterLink>
                                                            </div>
                                                        </template>
                                                    </v-checkbox>
                                                </div>
                                            </template>
                                            <div class="exchange-data__submit">
                                                <v-btn
                                                    type="submit"
                                                    size="large"
                                                    :loading="loading"
                                                    :disabled="loading">
                                                    Перейти к оплате
                                                </v-btn>
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
    <status-modal
        v-model="statusModal.modelValue"
        :status="statusModal.status"
        :msg="statusModal.msg"
    ></status-modal>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapMutations, mapGetters, mapActions} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'ExchangeView',
    data() {
        return {
            search: {
                give: '',
                get: '',
            },
            tabs: [],
            activeTab: 'step1',
            loading: false,
            currencies: null,
            giveCurrency: null,
            getCurrency: null,
            changeForm: false,
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
            allCurrenciesApi: [],
            currenciesApi: {
                banks: [],
                crypto: [],
            },
            rules: {
                required: value => !!value || 'Обязательно для заполнения',
                cardNumberRule: v => (v && v.length === 19) || 'Номер карты должен содержать 16 цифр',
                emailRules: [
                    v => !!v || 'Email обязателен',
                    v => /.+@.+\..+/.test(v) || 'Неверно указан E-mail',
                ],
            },
            cryptoWalletRule: {
                size: {
                    from: 38,
                    to: 42,
                },
                startWith: '',
            },
            statusModal: {
                modelValue: false,
                status: 'reject',
                msg: "Вы не прошли проверку на робота!<br>Сработала защита от спама.<br>Попробуйте ещё раз немного позднее",
            },
        }
    },
    created() {
        this.getApiCurriencies();
    },
    mounted() {
        this.tabs = document.querySelectorAll('[data-tab-id]');
        this.ttl().then(() => {
            this.formData.selectedGiveCurrency = this.getExchangeData.selectedGiveCurrency ?? '';
            this.formData.selectedGetCurrency = this.getExchangeData.selectedGetCurrency ?? '';
            if (this.getRequestFixedTime > 0 && this.formData.selectedGiveCurrency && this.formData.selectedGetCurrency) {
                this.whereAmI().then(() => {
                    if (this.getCurExchangeStep ) {
                        this.$router.push({
                            name: 'ExchangeSteps',
                        })
                    }
                });
            }
        });
    },
    components: {
        StatusModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/StatusModal"),
        }),
    },
    computed: {
        ...mapGetters([
            'getUuid',
            'getRequestFixedTime',
            'getCurExchangeStep',
            'getExchangeData',
        ]),
        getCurrencyName() {
            return this.getCurrency ? this.getCurrency.name : '';
        },
        giveCurrencyName() {
            return this.giveCurrency ? this.giveCurrency.name : '';
        },
        filteredGiveBanks() {
            return this.currenciesApi.banks.filter(item =>
                item.name.toLowerCase().includes(this.search.give.toLowerCase()) || item.tikker.toLowerCase().includes(this.search.give.toLowerCase())
            );
        },
        filteredGiveCryptos() {
            return this.currenciesApi.crypto.filter(item =>
                item.name.toLowerCase().includes(this.search.give.toLowerCase()) || item.tikker.toLowerCase().includes(this.search.give.toLowerCase())
            );
        },
        filteredGetBanks() {
            return this.currenciesApi.banks.filter(item =>
                item.name.toLowerCase().includes(this.search.get.toLowerCase()) || item.tikker.toLowerCase().includes(this.search.get.toLowerCase())
            );
        },
        filteredGetCryptos() {
            return this.currenciesApi.crypto.filter(item =>
                item.name.toLowerCase().includes(this.search.get.toLowerCase()) || item.tikker.toLowerCase().includes(this.search.get.toLowerCase())
            );
        },
    },
    watch: {
        getCurrency(newCur, oldCur) {
            let vm = this;
            if (this.giveCurrency.tikker !== this.getCurrency.tikker && newCur.tikker !== (oldCur ? oldCur.tikker : '')) {
                this.getExchangeRate(this.giveCurrency.tikker, this.getCurrency.tikker).then(result => {
                    vm.formData.exchangeRate = result;
                    vm.recalculate();
                });
            }
        },
        giveCurrency(newCur, oldCur) {
            let vm = this;
            if (this.giveCurrency.tikker !== this.getCurrency.tikker && newCur.tikker !== (oldCur ? oldCur.tikker : '')) {
                this.getExchangeRate(this.giveCurrency.tikker, this.getCurrency.tikker).then(result => {
                    vm.formData.exchangeRate = result;
                    vm.recalculate();
                });
            }
            if (newCur.type === 'crypto') {
                this.getCurrency = this.currenciesApi['banks'][0];
                this.changeForm = true;
            }
            if (newCur.type === 'fiat') {
                this.getCurrency = this.currenciesApi['crypto'][0];
                this.changeForm = false;
            }
        }
    },
    methods: {
        ...mapMutations([
            'setExchangeData',
            'setCurExchangeStep',
        ]),
        ...mapActions([
            'ttl',
            'whereAmI',
            'checkToken',
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

            if (results.valid) {
                const isRobot = !(await this.checkToken());
                if (isRobot) {
                    this.statusModal.modelValue = true;
                    this.loading = false;
                    return false;
                }
                this.formData.giveTikker = this.giveCurrency.tikker;
                this.formData.getTikker = this.getCurrency.tikker;
                this.formData.selectedGetCurrency = this.getCurrency.name;
                this.formData.selectedGiveCurrency = this.giveCurrency.name;
                this.setExchangeData(this.formData);
                let isDataSended = await this.sendData();
                if (isDataSended) {
                    await this.ttl()
                    this.setCurExchangeStep(1);
                    await this.confirmRequest();
                    this.$router.push({
                        name: 'ExchangeSteps',
                    });
                }
            } else {
                this.formData.rules.error = !this.formData.rules.value;
                this.formData.privacy.error = !this.formData.privacy.value;
            }
            this.loading = false;
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
        async confirmRequest() {
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);
            let response = await fetch('/api/exchange/confirm_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
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
                exchangeData.uuid = this.getUuid;

                this.setExchangeData(exchangeData);
            }
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
                    let calcValue = this.formData.give * this.formData.exchangeRate;
                    amount = Math.round(calcValue);
                    if (amount === 0) {
                        amount = calcValue.toFixed(2);
                    }
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
                    let calcValue = this.formData.get * this.formData.exchangeRate;
                    amount = Math.round(calcValue);
                    if (amount === 0) {
                        amount = calcValue.toFixed(2);
                    }
                } else {
                    amount = (this.formData.get / this.formData.exchangeRate).toFixed(8);
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
            if (this.getCurrency.type === 'crypto') {
                let startWith = this.getCurrency.wallet_starts;
                let regex = new RegExp(`^(${startWith})[A-Za-z0-9]{${this.getCurrency.symbols_min},${this.getCurrency.symbols_max}}$`);
                if (regex.test(this.formData.cryptoNumber)) {
                    return true;
                }
            }
            if (this.getCurrency.type === 'fiat') {
                let startWith = this.giveCurrency.wallet_starts;
                let regex = new RegExp(`^(${startWith})[A-Za-z0-9]{${this.giveCurrency.symbols_min},${this.giveCurrency.symbols_max}}$`);
                if (regex.test(this.formData.cryptoNumber)) {
                    return true;
                }
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
                if (item.type === 'Фиатная валюта') {
                    item.type = 'fiat';
                    this.currenciesApi.banks.push(item);
                } else {
                    item.type = 'crypto';
                    this.currenciesApi.crypto.push(item);
                }
            });
            this.giveCurrency = this.currenciesApi.banks[0];
            this.getCurrency = this.currenciesApi.crypto[0];
            this.allCurrenciesApi = this.currenciesApi.banks.concat(this.currenciesApi.crypto);
            return response;
        },
        async getExchangeRate(giveTikker, getTikker) {
            let response = await fetch('/api/exchange/' + giveTikker + '/' + getTikker);
            if (response.ok) {
                let result = await response.json();

                this.getCurrency['symbols_min'] = result.get.symbols_min;
                this.getCurrency['symbols_max'] = result.get.symbols_max;
                this.getCurrency['wallet_starts'] = result.get.wallet_starts.replace(/\s/g, '').split('или').join('|');

                this.giveCurrency['symbols_min'] = result.give.symbols_min;
                this.giveCurrency['symbols_max'] = result.give.symbols_max;
                this.giveCurrency['wallet_starts'] = result.give.wallet_starts.replace(/\s/g, '').split('или').join('|');

                return result['exchange_rate'] ?? null;
            } else {
                setTimeout(window.location.reload, 3000);
            }
            return 0;
        },
    },
});
</script>