<template>
    <div class="confirm">
        <v-sheet rounded class="confirm__sheet pa-3 rounded-t-0">
            <v-container fluid class="confirm__container">
                <v-row class="confirm__row">
                    <v-progress-circular
                        class="confirm__progress"
                        indeterminate
                        color="primary"
                        :width="5"
                        :size="30"
                    ></v-progress-circular>
                    <h2 class="confirm__title title title_h2 title_black mb-4 text-center ml-2">
                        {{getCurExchangeStatus ?? 'Верификация карты'}}
                    </h2>
                </v-row>
                <v-row class="confirm__row">
                    <p class="confirm__text text-center">Внимательно пока проверьте правильность заполненных данных!</p>
                </v-row>
                <v-row class="confirm__row">
                    <v-sheet class="confirm__table-sheet" rounded>
                        <CurExchangeTable class="confirm__table"></CurExchangeTable>
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
    name: 'VerificationView',

    data: () => ({
        loading: false,
    }),
    mounted() {
        this.checkVerification();
        this.getStatus().then(result => {
            if (!result) {
                this.$emit('error', 'Ошибка!', '', 'Не удалось отправить запрос');
            }
        });
    },
    components: {
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
    },
    methods: {
        ...mapActions([
            'getStatus',
        ]),
        async checkVerification() {
            this.loading = true;
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);

            let response = await fetch('/api/exchange/await', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                if (response.status === 200) {
                    let result = await response.json();
                    if (result.verified) {
                        this.$emit('complete');
                        this.$emit('nextStep');
                    } else {
                        this.$emit('error', 'Ваша заявка была отклонена', '', 'Ваша заявка была отклонена', 'Вы не прошли верификацию. ' + (result.reason ?? ''));
                    }
                } else {
                    this.$emit('error', 'Ошибка!', '', 'Не удалось отправить запрос');
                }
            } else {
                await this.checkVerification();
            }
            this.loading = false;
        },
    },
    computed: {
        ...mapGetters([
            'getVerificationFile',
            'getUuid',
            'getCurExchangeStatus',
        ]),
    }
});
</script>
