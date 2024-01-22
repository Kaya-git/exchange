<template>
    <div class="auth">
        <div class="auth__wrapper">
            <h2 class="auth__title title title_h2">Восстановление пароля</h2>
            <v-form class="auth__form" validate-on="submit lazy" @submit.prevent="submit">
                <v-container class="auth__form-container">
                    <v-row class="auth__form-row">
                        <v-text-field
                            v-model="formData.email"
                            label="Email"
                            type="email"
                            :rules="emailRules">
                        </v-text-field>
                    </v-row>
                    <v-row class="auth__form-row">
                        <v-btn
                            class="auth__btn"
                            type="submit"
                            size="x-large"
                            color="primary"
                            :loading="loading"
                            :disabled="loading">
                            Восстановить
                        </v-btn>
                    </v-row>
                </v-container>
            </v-form>
        </div>
    </div>
    <status-modal
        :model-value="statusModal.modelValue"
        :status="statusModal.status"
        :msg="statusModal.msg"
    ></status-modal>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
export default defineComponent({
    name: 'ForgotPassword',

    data: () => ({
        loading: false,
        statusModal: {
            modelValue: false,
            status: 'success',
            msg: "Вы успешно сменили пароль!",
        },
        formData: {
            email: '',
        },
        emailRules: [
            v => !!v || 'Email обязателен',
            v => /.+@.+\..+/.test(v) || 'Неверно указан E-mail',
        ],
    }),
    components: {
        StatusModal: defineAsyncComponent({
            loader: () => import("../Modal/StatusModal"),
        }),
    },
    methods: {
        async submit(event) {
            this.loading = true;

            const results = await event;

            if (results.valid) {
                await this.sendData();
            } else {
                this.loading = false;
            }
        },
        async sendData() {
            this.statusModal.modelValue = false;
            let body = {
                'email': this.formData.email,
            }
            let response = await fetch('/api/auth/forgot-password',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept':  'application/json',
                },
                body: JSON.stringify(body),
            });
            if (response.ok) {
                let result = await response.json();
                console.log(result);
                this.statusModal.msg = 'Вам отправлено письмо на почту для восстановления пароля!';
            } else {
                this.statusModal.msg = 'Ошибка! Проблемы с сервером';
                this.statusModal.status = 'reject';
            }
            this.statusModal.modelValue = true;
            this.loading = false;
        }
    }
});
</script>
