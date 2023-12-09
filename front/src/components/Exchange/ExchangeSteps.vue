<template>
    <div class="exchange-steps pt-8 px-2">
        <v-stepper :model-value="step" class="confirm__steps rounded-b-0">
          <v-stepper-header>
            <v-stepper-item
                title="Confirm"
                :value="1"
            ></v-stepper-item>

            <v-divider></v-divider>

            <v-stepper-item title="Request created" :value="2"></v-stepper-item>

            <v-divider></v-divider>

            <v-stepper-item title="Verifyed" :value="3"></v-stepper-item>

            <v-divider></v-divider>

            <v-stepper-item title="Payed" :value="4"></v-stepper-item>
          </v-stepper-header>
          <v-stepper-window>
              <v-stepper-window-item :value="1">
                  <confirm-view @nextStep="step++"></confirm-view>
              </v-stepper-window-item>
            <v-stepper-window-item :value="2">
              <verification-view @nextStep="step++"></verification-view>
            </v-stepper-window-item>
            <v-stepper-window-item :value="3">
              <request-view @nextStep="step++"></request-view>
            </v-stepper-window-item>
            <v-stepper-window-item :value="4"></v-stepper-window-item>
          </v-stepper-window>
        </v-stepper>
    </div>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import { mapGetters, mapMutations } from 'vuex';

export default defineComponent({
    name: 'ExchangeSteps',

    data: () => ({
        exchangeData: null,
        error: {
          'status': false,
          'message': '',
        },
        step: 1,
    }),
    created() {
        this.exchangeData = this.getExchangeData;
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
    },
    methods: {
        ...mapMutations([
          'setExchangeData',
        ]),
    },
    computed: {
        ...mapGetters([
            'getExchangeData'
        ]),
    }
});
</script>
