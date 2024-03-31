<template>
    <div class="payed">
        <v-sheet rounded class="payed__sheet pa-3 rounded-t-0">
            <v-container fluid class="payed__container">
                <v-row class="payed__row">
                    <v-progress-circular
                        class="payed__progress"
                        indeterminate
                        color="primary"
                        :width="5"
                        :size="30"
                    ></v-progress-circular>
                    <h2 class="payed__title title title_h2 title_black mb-4 text-center">
                        {{status ?? 'Проверка оплаты'}}
                    </h2>
                </v-row>
                <v-row class="payed__row">
                    <p class="payed__text text-center">Внимательно проверьте правильность заполненных данных!</p>
                </v-row>
                <v-row class="payed__row">
                    <v-sheet class="payed__table-sheet" rounded>
                        <CurExchangeTable class="payed__table"></CurExchangeTable>
                    </v-sheet>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters, mapActions} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'PayedView',

    data: () => ({
        timerId: null,
        status: "Проверка оплаты",
    }),
    components: {
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
    },
    created() {
        this.payed();
        this.checkStatus();
    },
    mounted() {
        this.timerId = setInterval(() => {
            this.checkStatus();
        }, 5000);
    },
    beforeUnmount() {
        if (this.timerId) {
            clearInterval(this.timerId);
        }
    },
    methods: {
        ...mapActions([
            'getStatus',
        ]),
        async payed() {
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);

            let response = await fetch('/api/exchange/payed', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (!response.ok) {
                this.$emit('error', 'Не удалось отправить запрос');
            }
        },
        async checkStatus() {
            let response = await fetch('/api/orders/get_order_status?user_uuid=' + this.getUuid);
            if (response.ok) {
                let result = await response.json();
                if (result.status) {
                    this.status = result.status;
                }
                if (result.link) {
                    this.$emit('complete', 'Отлично, обмен прошел УСПЕШНО', 'Ваша ссылка на транзакцию:');
                }
                if (result.reason) {
                    this.$emit('error', 'Отказано. ' + result.reason);
                }
            }
        }
    },
    computed: {
        ...mapGetters([
            'getUuid',
            'getCurExchangeStatus',
        ]),
    }
});
</script>
