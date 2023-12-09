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
                    <div class="confirm-modal__cardnumber">
                        <div class="confirm-modal__cardnumber-wrapper">
                            <span>{{requisite}} Денис Н.</span>
                        </div>
                    </div>
                </v-row>
                <v-row class="justify-center">
                    <p class="confirm-modal__text">Подтвердите перевод по указанным <br> выше реквизитам</p>
                </v-row>
                <v-row>
                    <v-col class="d-flex justify-end">
                        <v-btn size="large" color="success" @click="$emit('confirmed')">
                            Оплачено
                        </v-btn>
                    </v-col>
                    <v-col>
                        <v-btn size="large" color="error" @click="$emit('canceled')">Вернуться</v-btn>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'ConfirmTrade',
    props: {
        requisite: {
            type: String,
            default: '',
        },
    },
    data: () => ({

    }),
    emits: ['confirmed', 'canceled'],
});
</script>
