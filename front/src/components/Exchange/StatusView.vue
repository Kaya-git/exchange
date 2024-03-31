<template>
    <div class="status-page" style="position: relative;">
        <v-sheet rounded class="status-page__sheet pa-3 rounded-t-0">
            <v-container fluid class="status-page__container">
                <v-row class="status-page__row mb-4">
                    <h2 class="status-page__title title title_h2 title_black text-center">{{title}}</h2>
                    <v-icon class="status-page__title-icon ml-1" :color="statuses[status].color">
                        {{statuses[status].icon}}
                    </v-icon>
                </v-row>
                <v-row class="status-page__row">
                    <p class="status-page__text text-center">{{subtitle}}</p>
                </v-row>
                <v-row class="status-page__row">
                    <v-sheet class="status-page__table-sheet" rounded>
                        <CurExchangeTable class="status-page__table"></CurExchangeTable>
                        <v-card class="status-page__card">
                            <v-card-title class="status-page__card-title">Помогите нам и оставьте краткий отзыв!</v-card-title>
                            <v-card-text class="status-page__card-text">
                                Спасибо, что воспользовались нашим сервисом. <br>
                                Просим вас оставить отзыв о работе с нами.
                            </v-card-text>
                            <v-card-actions class="status-page__card-actions">
                                <ReviewModal btnColor="success"></ReviewModal>
                            </v-card-actions>
                        </v-card>
                    </v-sheet>
                </v-row>
                <v-row class="status-page__row">
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
                icon: 'mdi-checkbox-marked',
            },
            reject: {
                color: 'error',
                icon: 'mdi-alert-box',
            }
        }
    }),
    components: {
        CurExchangeTable: defineAsyncComponent({
            loader: () => import("@/components/Tables/CurExchangeTable"),
        }),
        ReviewModal: defineAsyncComponent({
            loader: () => import("@/components/Modal/ReviewModal"),
        }),
    },
});
</script>
