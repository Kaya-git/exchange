<template>
    <v-btn 
        class="reviews__btn" 
        size="large"
        :color="btnColor"
        @click="overlay = !overlay"
        append-icon="mdi-check-circle-outline">
            Оставить отзыв
        <template v-slot:append>
            <v-icon class="reviews__btn-icon flashing-icon" color="success"></v-icon>
        </template>
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
                    <div class="d-flex flex-column mb-4">
                        <v-label
                            class="review-modal__radio-label ml-4">
                            Оцените работу нашего сервиса
                        </v-label>
                        <v-rating
                            v-model="rating"
                            active-color="blue-lighten-2"
                            color="orange-lighten-1"
                        >
                        </v-rating>
                    </div>
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
    props: {
      btnColor: {
        type: String,
        default: '',
      }
    },
    data: () => ({
        overlay: false,
        loading: false,
        name: '',
        comment: '',
        rating: 0,
        commentRules: {
            required: v => !!v || 'Обязательное поле',
            lengthRule: v => (v && v.length <= 200) || 'Комментарий должен быть не более 200 символов',
        },
        rules: {
            required: value => !!value || 'Обязательно для заполнения',
        }
    }),
    mounted() {
        this.startFlashing();
    },
    methods: {
        async submit(event) {
            this.loading = true;

            const results = await event;

            if (results.valid) {
                let body = {
                    'name': this.name,
                    'text': this.comment,
                    'rating': this.rating,
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
                    this.rating = 0;
                    this.name = '';
                    this.comment = '';
                }
            }
            this.loading = false;
        },
        toggleIcon() {
            const icon = document.querySelector('.flashing-icon');
            if (icon) {
                icon.classList.toggle('flashing');
            }
        },
        startFlashing() {
            setInterval(() => {
                this.toggleIcon();
            }, 500);
        },
    }
});
</script>
