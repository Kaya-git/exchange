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
                    <confirm-view v-if="!steps[curStep].error" @nextStep="curStep++" @complete="completeStep" @error="errorStep"></confirm-view>
                    <error-view v-if="steps[curStep].error" :title="steps[curStep].message"
                                :subtitle="steps[curStep].subtitle"></error-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="2">
                    <verification-view @nextStep="curStep++" @complete="completeStep"
                                       @error="errorStep"></verification-view>
                    <error-view v-if="steps[curStep].error" :title="steps[curStep].message"
                                :subtitle="steps[curStep].subtitle"></error-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="3">
                    <request-view @nextStep="curStep++" @complete="completeStep" @error="errorStep"></request-view>
                    <error-view v-if="steps[curStep].error" :title="steps[curStep].message"
                                :subtitle="steps[curStep].subtitle"></error-view>
                </v-stepper-window-item>
                <v-stepper-window-item :value="4">
                    <status-view @complete="completeStep" @error="errorStep"></status-view>
                    <error-view v-if="steps[curStep].error" :title="steps[curStep].message"
                                :subtitle="steps[curStep].subtitle"></error-view>
                </v-stepper-window-item>
            </v-stepper-window>
        </v-stepper>
    </div>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters, mapMutations, mapActions} from 'vuex';

export default defineComponent({
    name: 'ExchangeSteps',

    data: () => ({
        exchangeData: null,
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
    created() {
        this.exchangeData = this.getExchangeData;
    },
    watch: {
        curStep(newStep, oldStep) {
            this.steps[oldStep].complete = true;
        }
    },
    components: {
        ConfirmView: defineAsyncComponent({
            loader: () => import("../Exchange/ConfirmView"),
        }),
        VerificationView: defineAsyncComponent({
            loader: () => import("../Exchange/VerificationView"),
        }),
        RequestView: defineAsyncComponent({
            loader: () => import("../Exchange/RequestView"),
        }),
        StatusView: defineAsyncComponent({
            loader: () => import("../Exchange/StatusView"),
        }),
        ErrorView: defineAsyncComponent({
            loader: () => import("../Exchange/ErrorView"),
        }),
    },
    methods: {
        ...mapMutations([
            'auth',
        ]),
        ...mapActions([
            'clearDataFromLocalStorage'
        ]),
        errorStep(message = '', subtitle = '') {
            this.steps[this.curStep].error = true;
            this.steps[this.curStep].color = 'error';
            this.steps[this.curStep].message = message;
            this.steps[this.curStep].subtitle = subtitle;
            this.clearDataFromLocalStorage();
        },
        completeStep() {
            this.steps[this.curStep].complete = true;
            this.steps[this.curStep].color = 'success';
        }
    },
    computed: {
        ...mapGetters([
            'getExchangeData'
        ]),
    }
});
</script>
