<template>
    <div class="auth">
      <div class="auth__wrapper">
        <h2 class="auth__title title title_h2">Авторизация</h2>
        <v-form class="auth__form" v-model="valid">
          <v-text-field
            v-model="formData.email"
            label="Email"
            type="email"
            required
          ></v-text-field>
          <v-text-field
            v-model="formData.password"
            label="Пароль"
            type="password"
            required
          ></v-text-field>
          <v-btn class="auth__btn" type="submit" size="large" color="primary">
            Войти
          </v-btn>
        </v-form>
      </div>
    </div>
  </template>
  
  <script>
  import {defineComponent} from 'vue';
  
  export default defineComponent({
    name: 'AuthView',
  
    data: () => ({
      valid: false,
      formData: {
        email: '',
        password: ''
      }
    }),
  });
  </script>
  