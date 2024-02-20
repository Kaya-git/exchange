<template>
    <div class="exchange-steps pt-8 px-2">
        <v-stepper :model-value="curStep" class="confirm__steps rounded-b-0">
            <v-stepper-header>
                <v-stepper-item
                    :value="1"
                    :color="steps[1].color"
                    :error="steps[1].error"
                    :complete="steps[1].complete"
                    :subtitle="steps[1].subtitle">
                    <template v-slot:title>
                        <span class="text-left"
                              style="display: block; width: 100%;">{{ steps[1].message ? steps[1].message : steps[1].title }}</span>
                    </template>
                </v-stepper-item>

                <v-divider></v-divider>

                <v-stepper-item
                    :value="2"
                    :complete="steps[2].complete"
                    :color="steps[2].color"
                    :error="steps[2].error"
                    :subtitle="steps[2].subtitle">
                    <template v-slot:title>
                        <span class="text-left"
                              style="display: block; width: 100%;">{{ steps[2].message ? steps[2].message : steps[2].title }}</span>
                    </template>
                </v-stepper-item>

                <v-divider></v-divider>

                <v-stepper-item
                    :value="3"
                    :complete="steps[3].complete"
                    :color="steps[3].color"
                    :error="steps[3].error"
                    :subtitle="steps[3].subtitle">
                    <template v-slot:title>
                        <span class="text-left"
                              style="display: block; width: 100%;">{{ steps[3].message ? steps[3].message : steps[3].title }}</span>
                    </template>
                </v-stepper-item>

                <v-divider></v-divider>

                <v-stepper-item
                    :value="4"
                    :complete="steps[4].complete"
                    :color="steps[4].color"
                    :error="steps[4].error"
                    :subtitle="steps[4].subtitle">
                    <template v-slot:title>
                        <span class="text-left"
                              style="display: block; width: 100%;">{{ steps[4].message ? steps[4].message : steps[4].title }}</span>
                    </template>
                </v-stepper-item>
            </v-stepper-header>
            <v-stepper-window>
                <v-stepper-window-item :value="1">
                    <confirm-view
                        v-if="!steps[curStep].error"
                        @nextStep="curStep++"
                        @complete="completeStep"
                        @error="errorStep"
                        @skip="skipStep"
                        @cancel="cancelExchange"></confirm-view>
                    <status-view v-if="steps[curStep].error"
                                :title="steps[curStep].message"
                                :subtitle="steps[curStep].subtitle"
                                status="reject"
                    ></status-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="2">
                    <verification-view @nextStep="curStep++" @complete="completeStep"
                                       @error="errorStep"></verification-view>
                    <status-view v-if="steps[curStep].error"
                                 :title="steps[curStep].message"
                                 :subtitle="steps[curStep].subtitle"
                                 status="reject"
                    ></status-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="3">
                    <request-view
                        @nextStep="curStep++"
                        @complete="completeStep"
                        @error="errorStep"
                        @cancel="cancelExchange"></request-view>
                    <status-view v-if="steps[curStep].error"
                                 :title="steps[curStep].message"
                                 :subtitle="steps[curStep].subtitle"
                                 status="reject"
                    ></status-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="4">
                    <payed-view v-if="!steps[curStep].complete && !steps[curStep].error" @complete="completeStep" @error="errorStep"></payed-view>
                    <status-view v-if="steps[curStep].error"
                                 :title="steps[curStep].message"
                                 :subtitle="steps[curStep].subtitle"
                                 status="reject"
                    ></status-view>
                    <status-view v-else-if="steps[curStep].message"
                                 :title="steps[curStep].message"
                                 :subtitle="steps[curStep].subtitle"
                                 status="success"
                    ></status-view>
                </v-stepper-window-item>
            </v-stepper-window>
        </v-stepper>
    </div>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters, mapActions} from 'vuex';
import {prepareData, deleteCookie} from '@/helpers';

export default defineComponent({
    name: 'ExchangeSteps',

    data: () => ({
        error: {
            'status': false,
            'message': '',
        },
        curStep: 1,
        steps: {
            1: {
                title: 'Подтверждение',
                complete: false,
                error: false,
                message: '',
                color: '',
                subtitle: '',
            },
            2: {
                title: 'Верификация',
                complete: false,
                error: false,
                message: '',
                color: '',
                subtitle: '',
            },
            3: {
                title: 'Заявка создана',
                complete: false,
                error: false,
                message: '',
                color: '',
                subtitle: '',
            },
            4: {
                title: 'Решение по заявке',
                complete: false,
                error: false,
                message: '',
                color: '',
                subtitle: '',
            },
        }
    }),
    mounted() {
        if (this.getCurExchangeStep) {
            if ([1, 2, 3].includes(Number(this.getCurExchangeStep))) {
                this.curStep = 1;
            } else if ([4, 5].includes(Number(this.getCurExchangeStep))) {
                this.curStep = 2;
            } else if ([6].includes(Number(this.getCurExchangeStep))) {
                this.curStep = 3;
            } else if ([7].includes(Number(this.getCurExchangeStep))) {
                this.curStep = 4;
            }
        }
    },
    watch: {
        curStep(newStep, oldStep) {
            this.steps[oldStep].complete = true;
        }
    },
    components: {
        ConfirmView: defineAsyncComponent({
            loader: () => import("@/components/Exchange/ConfirmView"),
        }),
        VerificationView: defineAsyncComponent({
            loader: () => import("@/components/Exchange/VerificationView"),
        }),
        RequestView: defineAsyncComponent({
            loader: () => import("@/components/Exchange/RequestView"),
        }),
        PayedView: defineAsyncComponent({
            loader: () => import("@/components/Exchange/PayedView"),
        }),
        StatusView: defineAsyncComponent({
            loader: () => import("@/components/Exchange/StatusView"),
        }),
    },
    methods: {
        ...mapActions([
            'clearDataFromLocalStorage'
        ]),
        errorStep(message = '', subtitle = '') {
            this.steps[this.curStep].error = true;
            this.steps[this.curStep].color = 'error';
            this.steps[this.curStep].message = message;
            this.steps[this.curStep].subtitle = subtitle;
            this.clearDataFromLocalStorage();
            deleteCookie('user_uuid');
        },
        completeStep(message = '',) {
            this.steps[this.curStep].complete = true;
            this.steps[this.curStep].color = 'success';
            this.steps[this.curStep].message = message;
        },
        skipStep() {
            let skippedStep = this.curStep + 1;
            this.completeStep();
            this.steps[skippedStep].complete = true;
            this.steps[skippedStep].color = 'success';
            this.curStep = this.curStep + 2;
        },
        async cancelExchange() {
            this.disabled = true;
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);
            let response = await fetch('/api/orders/decline_order', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                this.errorStep('Заявка отменена');
                this.clearDataFromLocalStorage();
            }
            this.disabled = false;
        },
    },
    computed: {
        ...mapGetters([
            'getCurExchangeStep',
            'getUuid',
        ]),
    }
});
</script>
