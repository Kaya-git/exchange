<template>
    <v-dialog
        persistent
        width="auto"
        class="wait-modal">
        <v-sheet
            class="wait-modal__sheet pa-4"
            rounded>
            <v-container fluid class="wait-modal__container">
                <v-row class="justify-center">
                    <h2 class="wait-modal__title title title_h2 title_black">
                        {{curMsg}}
                    </h2>
                </v-row>
                <v-row class="justify-center">
                    <v-progress-circular
                        indeterminate
                        color="primary"
                        :width="6"
                        :size="50"
                    ></v-progress-circular>
                </v-row>
            </v-container>
        </v-sheet>
    </v-dialog>
</template>

<script>
import {defineComponent} from 'vue';
import {randomInteger} from '@/helpers';

export default defineComponent({
    name: 'WaitModal',
    props: {
        msg: {
            type: String,
            default: '',
        },
    },
    data: () => ({
        defaultMessages: [
            'Придется немного подождать',
            'Проверка безопасности',
        ],
        curMsg: null,
        timer: null,
    }),
    created() {
        this.newMessage();
        this.timer = setInterval(() => {
            this.newMessage();
        }, 5000);
    },
    beforeUnmount() {
        if (this.timer) {
            clearInterval(this.timer);
        }
    },
    methods: {
        newMessage() {
            this.curMsg = this.defaultMessages[randomInteger(0,this.defaultMessages.length - 1)];
        }
    }
});
</script>
