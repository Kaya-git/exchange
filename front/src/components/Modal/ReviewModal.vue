<template>
    <v-btn 
        class="reviews__btn" 
        size="large"
        @click="overlay = !overlay">
            Оставить отзыв
    </v-btn>
    <v-overlay 
        v-model="overlay"
        class="review-modal align-center justify-center">
        <v-sheet 
            class="review-modal__sheet pa-4"
            rounded>
            <v-container fluid class="review-modal__container">
                <h2 
                class="review-modal__title title title_h2 title_black mb-4 text-center">
                    Оставить отзыв
                </h2>
                <v-form class="review-modal__form" validate-on="submit lazy" @submit.prevent="submit">
                    <v-text-field
                        class="review-modal__input"
                        v-model="name"
                        :rules="[rules.required]"
                        label="Имя"></v-text-field>
                    <v-radio-group 
                    v-model="radios" 
                    class="ma-0">
                        <template
                        v-slot:label>
                            <div 
                            class="review-modal__radio-label">
                                Оцените работу нашего сервиса
                            </div>
                        </template>
                        <v-radio
                        label="Довольны"
                        color="green"
                        value="good"></v-radio>
                        <v-radio
                        label="Недовольны"
                        color="red"
                        value="bad"></v-radio>
                    </v-radio-group>
                    <v-textarea
                    class="review-modal__input"
                    v-model="comment"
                    label="Комментарий"
                    :rules="[commentRules.required, commentRules.lengthRule]"
                    ></v-textarea>
                    <v-btn 
                    color="success" 
                    class="review-modal__submit mt-4" 
                    block
                    :loading="loading"
                    type="submit">
                        Отправить
                    </v-btn>
                </v-form>
            </v-container>
        </v-sheet>
    </v-overlay>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
name: 'ReviewModal',
    data: () => ({
        overlay: false,
        loading: false,
        name: '',
        comment: '',
        radios: 'good',
        commentRules: {
            required: v => !!v || 'Обязательное поле',
            lengthRule: v => (v && v.length <= 200) || 'Комментарий должен быть не более 200 символов',
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
    methods: {
        async submit(event) {
            this.loading = true;

            const results = await event;

            if (results.valid) {
                let body = {
                    'name': this.name,
                    'text': this.comment,
                    'rating': this.radios === 'good' ? 5 : 1,
                }
                let response = await fetch('/api/reviews/review_form', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'accept':  'application/json',
                    },
                    body: JSON.stringify(body),
                });
                if (response.ok) {
                    this.overlay = false;
                }
            }
            this.loading = false;
        }
    }
});
</script>
