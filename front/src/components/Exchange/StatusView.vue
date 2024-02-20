<template>
    <div class="status-page">
        <v-sheet rounded class="status-page__sheet pa-3 rounded-t-0">
            <v-container fluid class="status-page__container">
                <v-row class="status-page__row">
                    <h2 class="status-page__title title title_h2 title_black mb-4 text-center">{{title}}</h2>
                </v-row>
                <v-row class="status-page__row">
                    <p class="status-page__text text-center">{{subtitle}}</p>
                </v-row>
                <v-row class="status-page__row">
                    <v-sheet class="status-page__table-sheet" rounded>
                        <CurExchangeTable class="status-page__table"></CurExchangeTable>
                    </v-sheet>
                </v-row>
                <v-row>
                    <v-col class="d-flex justify-center">
                        <RouterLink to="/">
                            <v-btn size="large" :color="statuses[status].color">На главную</v-btn>
                        </RouterLink>
                    </v-col>
                </v-row>
            </v-container>
        </v-sheet>
    </div>
</template>
<script>
import {defineComponent, defineAsyncComponent} from 'vue';

export default defineComponent({
    name: 'StatusView',
    props: {
        subtitle: {
            type: String,
            default: '',
        },
        title: {
            type: String,
            default: '',
        },
        status: {
            type: String,
            default: 'success',
        },
    },
    data: () => ({
        statuses: {
            success: {
                color: 'success',
            },
            reject: {
                color: 'error',
            }
        }
    }),
    components: {
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
    },
});
</script>
