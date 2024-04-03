<template>
    <v-dialog
        width="auto"
        persistent
        class="verification-modal align-center justify-center">
        <v-sheet
            class="verification-modal__sheet pa-4"
            rounded>
            <v-container fluid class="verification-modal__container">
                <v-form validate-on="submit lazy" @submit.prevent="verify">
                    <v-row class="justify-center">
                        <h2 class="verification-modal__title title title_h2 title_black mb-4">Верификация</h2>
                    </v-row>
                    <v-row class="justify-center mb-4">
                        <p class="verification-modal__text">Введите токен, который пришел вам на указанную почту</p>
                    </v-row>
                    <v-row>
                        <v-text-field
                            class="verification-form__field"
                            v-model="formData.token"
                            label="Токен"
                            type="text"
                        ></v-text-field>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex justify-end">
                            <v-btn size="large" color="success" type="submit" :loading="loading" :disabled="loading">
                                Подтвердить
                            </v-btn>
                        </v-col>
                        <v-col>
                            <v-btn
                                size="large"
                                color="error"
                                :disabled="loading"
                                @click="$emit('canceled')">
                                Отменить
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import {mapMutations} from 'vuex';

export default defineComponent({
    name: 'VerifyEmail',
    data: () => ({
        formData: {
            token: '',
        },
        rules: [
            v => !!v || 'Обязательное поле',
            v => v.length < 4 || 'Введите 4 символа',
        ],
        loading: false,
    }),
    emits: ['canceled', 'error', 'success'],
    methods: {
        ...mapMutations([
            'setVerificationFile',
        ]),
        async verify(event) {
            this.loading = true;
            const results = await event;
            if (!results.valid) {
                return false;
            }
            let isDataSended = await this.sendData();
            if (!isDataSended) {
                return false;
            }
            this.$emit('success');
            this.loading = false;
        },
        async sendData() {
            let response = await fetch('/api/email_verif/verif?verif_token=' + this.formData.token, {
                method: 'GET',
                headers: {
                    'accept':  'application/json',
                },
            });
            if (!response.ok) {
                this.$emit('error');
            }
            return await response.json();
        }
    }
});
</script>
