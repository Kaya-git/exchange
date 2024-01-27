<template>
    <v-dialog
        width="auto"
        class="status-modal align-center justify-center">
        <v-sheet
            class="status-modal__sheet pa-4"
            rounded>
            <v-container fluid class="status-modal__container">
                <v-row class="justify-center">
                    <v-icon
                        class="status-modal__icon"
                        :icon="icons[status].src"
                        :color="icons[status].color"></v-icon>
                </v-row>
                <v-row class="justify-center">
                    <p class="status-modal__text" v-html="msg"></p>
                </v-row>
                <v-row class="justify-end" v-if="btn">
                    <v-btn
                        class="status-modal__btn"
                        :color="status"
                        block
                        @click="$emit('close')">
                        {{btn}}
                    </v-btn>
                </v-row>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'StatusModal',
    props: {
        status: {
            type: String,
            default: 'success',
        },
        msg: {
            type: String,
            default: '',
        },
        btn: {
            type: String,
            default: '',
        }
    },

    data: () => ({
        icons: {
            success: {
                src: 'mdi-check-circle-outline',
                alt: 'success',
                color: 'green-darken-2'
            },
            reject: {
                src: 'mdi-alert-outline',
                alt: 'error',
                color: 'red-darken-2',
            },
        }
    }),
    emits: ['close']
});
</script>
