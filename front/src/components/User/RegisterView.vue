<template>
    <div class="register">
      <div class="register__wrapper">
        <h2 class="register__title title title_h2">Регистрация</h2>
        <v-form class="register__form" validate-on="submit lazy" @submit.prevent="submit">
            <v-container class="register__form=container">
                <v-row class="register__form-row">
                    <v-text-field
                        v-model="formData.email"
                        label="Email"
                        type="email"
                        :rules="[rules.required]"
                    ></v-text-field>
                </v-row>
                <v-row class="register__form-row">
                    <v-text-field
                        v-model="formData.password"
                        label="Пароль"
                        :rules="[rules.required]"
                        :type="show ? 'text' : 'password'"
                        :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                        @click:append-inner="show = !show"
                    ></v-text-field>
                </v-row>
                <v-row class="register__form-row mt-0">
                    <div class="register__form-details">
                        <v-checkbox
                            hide-details
                            :rules="[rules.required]">
                            <template v-slot:label>
                                <span>Я согласен с <RouterLink to="/privacy/">условиями правилами сервиса</RouterLink></span>
                            </template>
                        </v-checkbox>
                    </div>
                </v-row>
                <v-row class="register__form-row">
                    <v-btn
                        class="register__btn"
                        type="submit"
                        size="large"
                        color="primary"
                        :loading="loading"
                        :disabled="loading">
                        Зарегистрироваться
                    </v-btn>
                </v-row>
                <v-row class="register__form-row">
                    <div class="register__form-auth">
                        <span>Уже есть аккаунт? <RouterLink to="/auth/">Войдите</RouterLink></span>
                    </div>
                </v-row>
            </v-container>
        </v-form>
      </div>
    </div>
    <verify-email
    v-model="verifyModalShow"
    @canceled="verifyModalShow = !verifyModalShow"
    ></verify-email>
    <status-modal
        v-model="statusModal.modelValue"
        :status="statusModal.status"
        :msg="statusModal.msg"
    ></status-modal>
</template>
  
<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapMutations} from 'vuex';
export default defineComponent({
    name: 'RegisterView',

    data: () => ({
        loading: false,
        show: false,
        verifyModalShow: false,
        statusModal: {
            modelValue: false,
            status: 'success',
            msg: "Вы успешно зарегистрировались!<br>Вам отправлено сообщение на почту для её подтверждения",
        },
        sended: false,
        formData: {
            email: '',
            password: '',
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
    components: {
        VerifyEmail: defineAsyncComponent({
            loader: () => import("@/components/Modal/VerifyEmail"),
        }),
        StatusModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/StatusModal"),
        }),
    },
    watch: {
        'statusModal.modelValue': function (newVal) {
            if (!newVal && this.sended) {
                this.$router.push({
                    name: 'AuthView',
                });
            }
        }
    },
    methods: {
        ...mapMutations([
            'setUserEmail',
        ]),
        async submit(event) {
            this.loading = true;

            const results = await event;

            if (results.valid) {
                let isDataSended = await this.sendData();
                if (isDataSended) {
                    this.statusModal.modelValue = true;
                    this.sended = true;
                }
            }
            this.loading = false;
        },
        async sendData() {
            let body = {
                'email': this.formData.email,
                'password': this.formData.password,
                "is_active": true,
                "is_superuser": false,
                "is_verified": false
            }

            let response = await fetch('/api/auth/register',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept':  'application/json',
                },
                body: JSON.stringify(body),
            });
            if (response.ok) {
                return await response.json();

            }
            return false;
        },
    }
});
</script>
