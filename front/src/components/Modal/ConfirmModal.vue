<template>
    <v-dialog
        width="auto"
        persistent
        class="confirm-modal align-center justify-center">
        <v-sheet
            class="confirm-modal__sheet pa-4"
            rounded>
            <v-container fluid class="confirm-modal__container">
                <v-row class="justify-center">
                    <p class="confirm-modal__text">
                        {{ msg }}
                        <v-icon class="confirm-modal__btn-icon ml-1" color="success">
                            mdi-check-circle-outline
                        </v-icon>
                    </p>
                </v-row>
                <v-row>
                    <v-col class="d-flex justify-center">
                        <v-btn
                            size="large"
                            color="success"
                            :loading="loading"
                            :disabled="loading"
                            @click="$emit('confirmed')">
                            {{ successMsg }}
                        </v-btn>
                    </v-col>
                    <v-col class="d-flex justify-center">
                        <v-btn
                            size="large"
                            color="error"
                            :disabled="loading"
                            @click="$emit('canceled')">
                            {{ rejectMsg }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'ConfirmModal',
    props: {
        msg: {
            type: String,
            default: '',
        },
        successMsg: {
            type: String,
            default: 'Подтвердить',
        },
        rejectMsg: {
            type: String,
            default: 'Отмена',
        },
        loading: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['confirmed', 'canceled'],
    data: () => ({

    }),
});
</script>
