<template>
    <div :class="customClass" class="timer">
        {{ formattedTime }}
    </div>
</template>

<script>
import {defineComponent} from 'vue';
import { mapActions, mapState} from 'vuex';

export default defineComponent({
    name: 'TimerView',
    props: {
        init: {
            type: Number,
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
        startTime: Math.round(new Date().getTime() / 1000),
    }),
    created() {
        if (this.init) {
            this.seconds = this.init;
        }
    },
    mounted() {
        this.startCountdown();
    },
    beforeUnmount() {
        clearInterval(this.timer);
    },
    methods: {
        ...mapActions([
            'clearDataFromLocalStorage',
        ]),
        startCountdown() {
            this.timer = setInterval(() => {
                if (this.seconds > 0) {
                    this.seconds--;
                } else {
                    this.clearDataFromLocalStorage();
                    clearInterval(this.timer); // Остановить таймер, когда время истекло
                    this.$emit('timeout');
                }
            }, 1000);
        },
    },
    computed: {
        ...mapState([
           'requestFixedTime',
        ]),
        formattedTime() {
            const minutes = Math.floor(this.seconds / 60);
            const sec = this.seconds % 60;
            return `${minutes.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`;
        },
    },
});
</script>