<template>
    <div class="reserves">
        <v-container class="reserves__container">
            <div class="reserves__content">
                <h1 class="reserves__title title title_h1">
                    Резервы валют
                </h1>
                <div class="reserves__cards">
                    <v-card class="reserves__card reserve-card">
                        <v-img 
                        class="reserve-card__img"
                        src="/icons/cryptos/bitcoin-btc-logo.svg"
                        ></v-img>
                        <v-card-title class="reserve-card__title">
                            Bitcoin
                        </v-card-title>
                        <v-card-subtitle class="reserve-card__subtitle">
                            100 BTC
                        </v-card-subtitle>
                    </v-card>
                    <v-card class="reserves__card reserve-card">
                        <v-img 
                        class="reserve-card__img"
                        src="/icons/cryptos/ethereum-eth-logo.svg"
                        ></v-img>
                        <v-card-title class="reserve-card__title">
                            Ethereum
                        </v-card-title>
                        <v-card-subtitle class="reserve-card__subtitle">
                            200 ETH
                        </v-card-subtitle>
                    </v-card>
                    <v-card class="reserves__card reserve-card">
                        <v-img 
                        class="reserve-card__img"
                        src="/icons/cryptos/tether-usdt-logo.svg"
                        ></v-img>
                        <v-card-title class="reserve-card__title">
                            Tether
                        </v-card-title>
                        <v-card-subtitle class="reserve-card__subtitle">
                            150 USDT
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
    
}),
});
</script>
