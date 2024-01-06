<template>
    <v-form class="account-form">
        <div class="account-form__cols">
            <div class="account-form__col">
                <h2 class="account-form__title title title_h2 title_black mb-4">
                    Основные данные
                </h2>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.email"
                    label="Email"
                    type="email"
                ></v-text-field>
            </div>
            <div class="account-form__col">
                <h2 class="account-form__title title title_h2 title_black mb-4">
                    Изменить пароль
                </h2>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.password"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    label="Пароль"
                    :type="show1 ? 'text' : 'password'"
                    @click:append="show1 = !show1"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.newPassword"
                    :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    label="Новый пароль"
                    :type="show2 ? 'text' : 'password'"
                    @click:append="show2 = !show2"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.confirmPassword"
                    label="Подтвердите пароль"
                    :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="show3 ? 'text' : 'password'"
                    @click:append="show3 = !show3"
                ></v-text-field>
            </div>
        </div>
        <div class="account-form__btns">
            <v-btn
                class="account-form__submit"
                color="success"
                size="large"
                :disabled="loading"
                :loading="loading"
                @click.prevent="changePassword">
                Сохранить
            </v-btn>
            <v-btn
                class="account-form__logout"
                color="error"
                size="large"
                :disabled="loading"
                @click="logout">
                Выйти
            </v-btn>
        </div>
    </v-form>
</template>

<script>
import {defineComponent} from 'vue';
import {mapState, mapActions} from 'vuex';

export default defineComponent({
    name: 'AccountForm',

    data: () => ({
        valid: false,
        loading: false,
        show1: false,
        show2: false,
        show3: false,
        formData: {
            email: '',
            password: '',
            newPassword: '',
            confirmPassword: '',
        }
    }),
    mounted() {
        this.formData.email = this.user.email;
        this.resizeBg();
    },
    methods: {
        ...mapActions([
            'resizeBg',
            'logout',
        ]),
        async changePassword() {
            this.loading = true;
            let body = {
                'old_pass': this.formData.password,
                'new_pass': this.formData.newPassword,
            }
            let response = await fetch('/api/lk/pass_change', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept': 'application/json',
                },
                body: JSON.stringify(body)
            });
            if (response.ok) {
                let result = await response.json();
                console.log(result);
            }
            this.loading = false;
        }
    },
    computed: {
        ...mapState([
            'user'
        ])
    }
});
</script>