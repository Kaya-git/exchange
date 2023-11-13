<template>
    <v-tabs class="account-nav">
        
    </v-tabs>
</template>

<script>
import {defineComponent} from 'vue';

export default defineComponent({
    name: 'AccountNav',

    data: () => ({
        valid: false,
        formData: {
            email: '',
            password: ''
        }
    }),
});
</script>