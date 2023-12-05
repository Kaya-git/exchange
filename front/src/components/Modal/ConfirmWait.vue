<template>
    <v-dialog
        width="auto"
        persistent
        class="wait-modal align-center justify-center">
        <v-sheet
            v-if="!confirmed"
            class="wait-modal__sheet pa-4"
            rounded>
            <v-container fluid class="wait-modal__container">
                <v-row>
                    <h2 
                class="wait-modal__title title title_h2 title_black mb-4 text-center">
                    Ожидание подтверждения заявки
                </h2>
                </v-row>
                <v-row class="justify-center">
                    <v-progress-circular
                    indeterminate
                    color="primary"
                    ></v-progress-circular>
                </v-row>
            </v-container>
        </v-sheet>
        <v-sheet
            v-else
            class="wait-modal__sheet pa-4"
            rounded>
            <v-container fluid class="wait-modal__container">
                <v-row>
                    <h2 class="wait-modal__title title title_h2 title_black mb-4 text-center">
                        Перевод подтвержден
                    </h2>
                </v-row>
                <v-row class="justify-center">
                    <v-icon
                    class="wait-modal__icon"
                    color="green-darken-2"
                    icon="mdi-check-circle"></v-icon>
                </v-row>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import { mapMutations } from 'vuex';

export default defineComponent({
name: 'ConfirmWait',
    data: () => ({
        confirmed: false,
    }),
    mounted() {
        this.waitConfirm();
    },
    methods: {
        ...mapMutations([
            'closeWaitOverlay',
        ]),
        waitConfirm() {
            setTimeout(() => {
                this.confirmed = true;
                setTimeout(() => {
                    this.closeWaitOverlay();
                    this.$router.push({name: 'ExchangeView'});
                }, 3000);
            }, 3000);
        }
    }
});
</script>
