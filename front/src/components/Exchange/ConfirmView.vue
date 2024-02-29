<template>
    <div class="confirm">
        <v-sheet rounded class="confirm__sheet pa-3 rounded-t-0">
            <v-container fluid class="confirm__container">
                <v-row class="confirm__row">
                    <h2 class="confirm__title title title_h2 title_black mb-4 text-center">
                        Подтвердите создание
                        заявки
                    </h2>
                </v-row>
                <v-row class="confirm__row">
                    <p class="confirm__text text-center">Внимательно проверьте правильность заполненных данных!</p>
                </v-row>
                <v-row class="confirm__row">
                    <v-sheet class="confirm__table-sheet" rounded>
                        <CurExchangeTable class="confirm__table"></CurExchangeTable>
                    </v-sheet>
                </v-row>
                <v-row class="confirm__row mb-8 flex-column align-center">
                    <p class="confirm__text text-center mb-4">
                        Курс зафиксирован на 10 минут, до отмены подтверждения заявки:
                    </p>
                    <timer-view
                        :custom-class="'confirm__timer'"
                        :init="getRequestFixedTime"
                        @timeout="$emit('error', 'Время подтверждения заявки вышло')"></timer-view>
                </v-row>
                <v-row class="confirm__row">
                    <v-col class="d-flex justify-sm-end justify-center">
                        <v-btn
                            @click="isModalVisible = true"
                            color="success"
                            class="confirm__btn"
                            :disabled="disabled"
                            size="large">
                            Создать заявку
                        </v-btn>
                    </v-col>
                    <v-col class="d-flex justify-sm-start justify-center">
                        <v-btn
                            class="confirm__reject-btn"
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
    <confirm-modal
        :model-value="isModalVisible"
        :msg="'Подтвердите, что введенные данные верны'"
        :loading="loading"
        @confirmed="confirm"
        @canceled="isModalVisible = !isModalVisible">
    </confirm-modal>
    <verification-modal
        :model-value="isVerificationModalVisible"
        :msg="'Загрузите фото для верификации вашей карты'"
        :loader="loading"
        @confirmed="verification"
        @canceled="isVerificationModalVisible = !isVerificationModalVisible"
    ></verification-modal>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapGetters} from 'vuex';
import {prepareData} from '@/helpers';

export default defineComponent({
    name: 'ConfirmView',

    data: () => ({
        error: {
            'status': false,
            'message': '',
        },
        isModalVisible: false,
        isVerificationModalVisible: false,
        loading: false,
        disabled: false,
    }),
    components: {
        TimerView: defineAsyncComponent({
            loader: () => import("@/components/Utils/TimerView"),
        }),
        ConfirmModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/ConfirmModal"),
        }),
        VerificationModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/VerificationModal"),
        }),
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
    },
    methods: {
        async confirm() {
            this.loading = true;
            let details = {
                'user_uuid': this.getUuid,
            }
            let formBody = prepareData(details);
            let response = await fetch('/api/exchange/confirm_button', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                },
                body: formBody
            });
            if (response.ok) {
                let result = await response.json();
                if (result.verified) {
                    this.$emit('skip');
                } else {
                    this.isVerificationModalVisible = true;
                }
            } else {
                this.$emit('error', 'Не удалось отправить запрос');
            }
            this.isModalVisible = false;
            this.loading = false;
        },
        async verification() {
            this.loading = true;
            const formData = new FormData();
            formData.append('user_uuid', this.getUuid);
            formData.append('cc_image', this.getVerificationFile);
            let response = await fetch('/api/exchange/cc_conformation_form', {
                method: 'POST',
                body: formData
            });
            this.isVerificationModalVisible = false;
            if (response.ok) {
                this.$emit('complete');
                this.$emit('nextStep');
            } else {
                this.$emit('error', 'Не удалось отправить запрос');
            }
            this.loading = false;
        },
        async cancel() {
            this.disabled = true;
            await this.$emit('cancel');
            this.disabled = false;
        }
    },
    computed: {
        ...mapGetters([
            'getVerificationFile',
            'getUuid',
            'getRequestFixedTime',
        ]),
    },
});
</script>
