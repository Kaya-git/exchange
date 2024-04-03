<template>
    <div class="reserves">
        <v-container class="reserves__container">
            <div class="reserves__content">
                <h1 class="reserves__title title title_h1">
                    Резервы валют
                </h1>
                <div class="reserves__cards">
                    <v-card
                        class="reserves__card reserve-card"
                        v-for="(reserve, i) in reserves"
                        :key="i">
                        <v-img
                            class="reserve-card__img"
                            :src="'/' + reserve.icon"
                        ></v-img>
                        <v-card-title class="reserve-card__title">
                            {{reserve.name}}
                        </v-card-title>
                        <v-card-subtitle class="reserve-card__subtitle">
                            {{reserve.reserve}} {{reserve.tikker}}
                        </v-card-subtitle>
                    </v-card>
                </div>
            </div>
        </v-container>
    </div>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'ReservesView',

    data: () => ({
        reserves: [],
    }),
    created() {
        this.getReserves();
    },
    mounted() {
    },
    methods: {
        async getReserves() {
            let response = await fetch('/api/currency/list');
            if (response.ok && response.status === 200) {
                this.reserves = await response.json();
                if (this.reserves.length) {
                    this.reserves = this.reserves.filter(function (item) {
                        if (item.type == 'Крипто-валюта') {
                            return true;
                        }
                        return false;
                    });
                }
            }
        }
    },
});
</script>
