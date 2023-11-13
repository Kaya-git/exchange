<template>
    <v-form class="account-form">
        <div class="account-form__cols">
            <div class="account-form__col">
                <h2 class="account-form__title title title_h2 title_black mb-4">
                    Основные данные
                </h2>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.login"
                    label="Логин"
                    type="text"
                ></v-text-field>
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
                    label="Пароль"
                    type="password"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.newPassword"
                    label="Новый пароль"
                    type="password"
                ></v-text-field>
                <v-text-field
                    class="account-form__field"
                    v-model="formData.confirmPassword"
                    label="Подтвердите пароль"
                    type="password"
                ></v-text-field>
            </div>
        </div>
        <v-btn 
        class="account-form__submit" 
        color="success"
        size="large">Сохранить</v-btn>
    </v-form>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'AccountForm',

    data: () => ({
        valid: false,
        formData: {
            login: '',
            email: '',
            password: '',
            newPassword: '',
            confirmPassword: '',
        }
    }),
});
</script>