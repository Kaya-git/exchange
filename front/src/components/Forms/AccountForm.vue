<template>
    <v-form class="account-form" validate-on="submit lazy" @submit.prevent="submit">
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
                    readonly
                ></v-text-field>
            </div>
            <div class="account-form__col">
                <h2 class="account-form__title title title_h2 title_black mb-4">
                    Изменить пароль
                </h2>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.password"
                    :append-inner-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    label="Пароль"
                    :type="show1 ? 'text' : 'password'"
                    :rules="[rules.required]"
                    @click:append-inner="show1 = !show1"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.newPassword"
                    :append-inner-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                    label="Новый пароль"
                    :type="show2 ? 'text' : 'password'"
                    :rules="[rules.required]"
                    @click:append-inner="show2 = !show2"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.confirmPassword"
                    label="Подтвердите пароль"
                    :append-inner-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="show3 ? 'text' : 'password'"
                    :rules="[rules.required]"
                    @click:append-inner="show3 = !show3"
                ></v-text-field>
            </div>
        </div>
        <div class="account-form__btns">
            <v-btn
                class="account-form__submit"
                size="large"
                type="submit"
                :disabled="loading"
                :loading="loading">
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
    <status-modal
        :model-value="statusModal.modelValue"
        :status="statusModal.status"
        :msg="statusModal.msg"
    ></status-modal>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';
import {mapState, mapActions} from 'vuex';

export default defineComponent({
    name: 'AccountForm',

    data: () => ({
        valid: false,
        loading: false,
        statusModal: {
            modelValue: false,
            status: 'success',
            msg: "Вы успешно сменили пароль!",
        },
        show1: false,
        show2: false,
        show3: false,
        formData: {
            email: null,
            password: null,
            newPassword: null,
            confirmPassword: null,
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
    mounted() {
        this.formData.email = this.user.email;
    },
    components: {
        StatusModal: defineAsyncComponent({
            loader: () => import("../Modal/StatusModal"),
        }),
    },
    methods: {
        ...mapActions([
            'logout',
        ]),
        async submit(event) {
            this.loading = true;
            this.statusModal.modelValue = false;
            const results = await event;
            if (results.valid) {
                await this.changePassword();
            }
            this.loading = false;
        },
        async changePassword() {
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
                this.formData.newPassword = '';
                this.formData.confirmPassword = '';
                this.statusModal.modelValue = true;
                return result;
            } else {
                this.statusModal.status = 'reject';
                this.statusModal.msg = 'Ошибка смены пароля';
            }
            this.statusModal.modelValue = true;
            return false;
        }
    },
    computed: {
        ...mapState([
            'user'
        ])
    }
});
</script>