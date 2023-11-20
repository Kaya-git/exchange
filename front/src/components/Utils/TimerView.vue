<template>
    <div :class="customClass" class="timer">
        {{ formattedTime }}
    </div>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'TimerView',
    props: {
        init: {
            type: Number,
            default: null,
        },
        route: {
            type: String,
            default: null,
        },
        customClass: {
            type: String,
            default: ""
        }
    },
    data: () => ({
        seconds: 600,
        timer: null,
    }),
    created() {
        if (this.init) {
            this.seconds = this.init;
        }
        this.startCountdown();
    },
    beforeUnmount() {
        clearInterval(this.timer);
    },
    methods: {
        startCountdown() {
            this.timer = setInterval(() => {
                if (this.seconds > 0) {
                    this.seconds--;
                } else {

                clearInterval(this.timer); // Остановить таймер, когда время истекло
                
                if (this.route) {
                    // this.$router.push({name: 'ExchangeView'});
                }
                }
            }, 1000);
        }
    },
    computed: {
        formattedTime() {
        const minutes = Math.floor(this.seconds / 60);
        const sec = this.seconds % 60;
        return `${minutes.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
        }
    },
});
</script>