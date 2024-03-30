<template>
    <v-dialog
        width="auto"
        persistent
        class="verification-modal align-center justify-center">
        <v-sheet
            class="verification-modal__sheet pa-4"
            rounded>
            <v-container fluid class="verification-modal__container">
                <v-form validate-on="submit lazy" @submit.prevent="confirm">
                    <v-row class="justify-center">
                        <h2 class="verification-modal__title title title_h2 title_black mb-4">Верификация карты</h2>
                    </v-row>
                    <v-row class="justify-center">
                        <p class="verification-modal__text">{{ msg }}</p>
                    </v-row>
                    <v-row>
                        <v-file-input
                            v-model="file"
                            :rules="rules"
                            show-size
                            accept="image/png, image/jpeg, image/bmp"
                            prepend-icon="mdi-camera"
                            label="Загрузите фото">
                        </v-file-input>
                    </v-row>
                    <v-row>
                        <v-col class="d-flex justify-end">
                            <v-btn size="large" color="success" type="submit" :loading="loading || loader" :disabled="loading || loader">
                                {{ successMsg }}
                            </v-btn>
                        </v-col>
                        <v-col>
                            <v-btn
                                size="large"
                                color="error"
                                :disabled="loading || loader"
                                @click="$emit('canceled')">{{ rejectMsg }}
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-form>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import {mapMutations} from 'vuex';

export default defineComponent({
    name: 'VerificationModal',
    props: {
        msg: {
            type: String,
            default: '',
        },
        successMsg: {
            type: String,
            default: 'Отправить',
        },
        rejectMsg: {
            type: String,
            default: 'Отмена',
        },
        loader: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['confirmed', 'canceled'],
    data: () => ({
        file: null,
        rules: [
            v => !!v || 'Обязательное поле',
            v => !!v.length || 'Пустой файл!',
            v => v[0].size < 4000000 || 'Размер фото должен быть меньше 4 MB!',
        ],
        loading: false,
    }),
    methods: {
        ...mapMutations([
            'setVerificationFile',
        ]),
        async confirm(event) {
            this.loading = true;
            const results = await event;

            if (results.valid) {
                this.setVerificationFile(this.file[0]);
                this.$emit('confirmed');
            }
            this.loading = false;
        },
    }
});
</script>
