<template>
    <div class="request">
        <v-sheet rounded class="request__sheet pa-3 rounded-t-0">
            <v-container class="request__container">
                <v-row class="request__row">
                    <h2 class="request__title title title_h2 title_black">Оплатить заявку</h2>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-sheet class="request__table-sheet" rounded>
                        <CurExchangeTable class="request__table"></CurExchangeTable>
                    </v-sheet>
                </v-row>
                <v-row class="request__row mb-2">
                    <p class="request__text">Курс зафиксирован на 15 минут. Заявка отменится через:</p>
                </v-row>
                <v-row class="request__row mb-8">
                    <timer-view :custom-class="'request__timer'" :init="getRequestFixedTime" @timeout="$emit('error', 'Время заявки вышло')"></timer-view>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-expansion-panels
                        v-model="panels"
                        multiple>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                Шаг 1. Переведите {{ exchangeData.give ?? '' }} {{ exchangeData.giveTikker ?? '' }} c
                                указанной карты на:
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="confirm-modal__cardnumber">
                                    <div class="confirm-modal__cardnumber-wrapper">
                                        <span v-html="requisite"></span>
                                    </div>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                        <v-expansion-panel>
                            <v-expansion-panel-title>
                                Шаг 2. После перевода нажмите на кнопку "Оплачено"
                            </v-expansion-panel-title>
                            <v-expansion-panel-text>
                                <div class="request__expansion-text">
                                    <div class="request__expansion-text-wrapper">
                                        <span>После проверки оплаты, вы получите ссылку на транзакцию в течение 5-15 мин</span>
                                    </div>
                                </div>
                            </v-expansion-panel-text>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </v-row>
                <v-row class="request__row mb-2">
                    <v-col class="d-flex justify-end">
                        <v-btn
                            id="request-submit"
                            size="large"
                            color="success"
                            :disabled="disabled"
                            @click="this.confirmOverlay = true">
                            Оплачено
                        </v-btn>
                    </v-col>
                    <v-col>
                        <v-btn
                            size="large"
                            :disabled="disabled"
                            @click="cancel()"
                            color="error">
                            Отменить
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
    <confirm-trade
        :model-value="confirmOverlay"
        :requisite="requisite"
        @confirmed="confirmTrade"
        @canceled="confirmOverlay = !confirmOverlay"
    ></confirm-trade>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters, mapActions} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'RequestView',

    data: () => ({
        exchangeData: null,
        confirmOverlay: false,
        requisites: '',
        disabled: false,
        panels: [0]
    }),
    created() {
        this.exchangeData = this.getExchangeData;
        this.getRequisites();
    },
    mounted() {
        this.ttl();
    },
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("@/components/Utils/TimerView"),
        }),
        ConfirmTrade: defineAsyncComponent({
            loader: () => import("@/components/Modal/ConfirmTrade"),
        }),
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
    },
    methods: {
        ...mapActions([
            'ttl',
        ]),
        async getRequisites() {
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);
            let response = await fetch('/api/exchange/order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept':  'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                this.requisites = await response.json();
                if (!this.requisites) {
                    this.$emit('error', 'Сервер не смог предоставить реквизиты');
                }
            } else {
                this.$emit('error', 'Упс! Что-то пошло не так...');
            }
        },
        confirmTrade() {
            this.confirmOverlay = !this.confirmOverlay;
            this.$emit('complete');
            this.$emit('nextStep');
        },
        async cancel() {
            this.disabled = true;
            await this.$emit('cancel');
            this.disabled = false;
        }
    },
    computed: {
        ...mapGetters([
            'getExchangeData',
            'getUuid',
            'getRequestFixedTime',
        ]),
        requisite() {
            return this.requisites.requisites_num + "" + this.requisites.holder;
        }
    }
});
</script>
