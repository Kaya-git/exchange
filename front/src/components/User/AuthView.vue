<template>
    <div class="auth">
        <div class="auth__wrapper">
            <h2 class="auth__title title title_h2">Авторизация</h2>
            <v-form class="auth__form" validate-on="submit lazy" @submit.prevent="submit">
                <v-container class="auth__form-container">
                    <v-row class="auth__form-row">
                        <v-text-field
                            v-model="formData.email"
                            label="Email"
                            type="email"
                            :rules="[rules.required]"
                        ></v-text-field>
                    </v-row>
                    <v-row class="auth__form-row">
                        <v-text-field
                            v-model="formData.password"
                            label="Пароль"
                            :rules="[rules.required]"
                            :type="show ? 'text' : 'password'"
                            :append-inner-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                            @click:append-inner="show = !show"
                        ></v-text-field>
                    </v-row>
                    <v-row class="auth__form-row mt-0">
                        <div class="auth__form-details">
                            <v-checkbox
                                label="Запомнить меня"
                                hide-details>
                            </v-checkbox>
                            <RouterLink class="auth__form-forgot" to="/forgot/">
                                Забыли пароль?
                            </RouterLink>
                        </div>
                    </v-row>
                    <v-row class="auth__form-row">
                        <v-btn
                            class="auth__btn"
                            type="submit"
                            size="x-large"
                            :loading="loading"
                            :disabled="loading">
                            Войти
                        </v-btn>
                    </v-row>
                    <v-row class="auth__form-row">
                        <div class="auth__form-register">
                            <span>Еще нет аккаунта? <RouterLink to="/register/">Зарегистрируйтесь</RouterLink></span>
                        </div>
                    </v-row>
                </v-container>
            </v-form>
        </div>
    </div>
</template>

<script>
import {defineComponent} from 'vue';
import {setCookie, prepareData} from '@/helpers';
import {mapMutations } from 'vuex';
export default defineComponent({
    name: 'AuthView',

    data: () => ({
        loading: false,
        show: false,
        formData: {
            email: '',
            password: '',
            rememberMe: false,
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
    methods: {
        ...mapMutations([
            'auth',
            'setUserEmail',
        ]),
        async submit(event) {
            this.loading = true;

            const results = await event;

            if (results.valid) {
                let isDataSended = await this.sendData();
                if (isDataSended) {
                    this.$router.push({
                        name: 'AccountView',
                    });
                }
            } else {
                this.loading = false;
            }
        },
        async sendData() {
            let details = {
                'username': this.formData.email,
                'password': this.formData.password,
                'grant_type': '',
                'scope': '',
                'client_id': '',
                'client_secret': '',
            }
            let formBody = prepareData(details);

            let response = await fetch('/api/auth/jwt/login',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept':  'application/json',
                },
                body: formBody,
            });
            if (response.ok) {
                this.auth();
                this.setUserEmail(this.formData.email);
                setCookie('user_email', this.formData.email);
                localStorage.setItem('auth', 'true');
                this.$router.push({
                    name: 'AccountView',
                });
            } else {
                this.loading = false;
            }
        }
    }
});
</script>
  