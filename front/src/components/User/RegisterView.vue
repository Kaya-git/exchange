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
  </template>
  
<script>
import {defineComponent} from 'vue';
import {setCookie} from '@/helpers';
import {mapMutations} from 'vuex';
export default defineComponent({
    name: 'RegisterView',

    data: () => ({
        loading: false,
        show: false,
        formData: {
        email: '',
        password: ''
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
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
                    this.setUserEmail(this.formData.email);
                    setCookie('user_email', this.formData.email);
                    this.$router.push({
                        name: 'AccountView',
                    });
                }
            } else {
                this.loading = false;
            }
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
        }
    }
});
</script>
