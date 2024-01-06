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
                        {{msg}}
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

export default defineComponent({
    name: 'WaitModal',
    props: {
        msg: {
            type: String,
            default: 'Придется немного подождать',
        },
    },
    data: () => ({

    }),
});
</script>
