<template>
    <div class="register">
      <div class="register__wrapper">
        <h2 class="register__title title title_h2">Регистрация</h2>
        <v-form class="register__form" v-model="valid">
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
          <v-btn class="register__btn" type="submit" size="large" color="primary">
            Зарегистрироваться
          </v-btn>
        </v-form>
      </div>
    </div>
  </template>
  
  <script>
  import {defineComponent} from 'vue';
  
  export default defineComponent({
    name: 'RegisterView',
  
    data: () => ({
      valid: false,
      formData: {
        email: '',
        password: ''
      }
    }),
  });
  </script>
  