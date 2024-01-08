<template>
    <div class="account">
        <v-tabs v-model="tab" fixed-tabs class="account__tabs" align-tabs="center">
            <v-tab class="account__tab" :value="1">Мои заявки</v-tab>
            <v-tab class="account__tab" :value="2">Ваши карты/счета</v-tab>
            <v-tab class="account__tab" :value="3">Настройки</v-tab>
        </v-tabs>
        <v-window :touch="false" class="account__window" v-model="tab">
            <v-window-item class="account__window-item" :value="1">
                <v-container class="account__window-container" fluid>
                    <v-sheet class="account__window-sheet pa-4 pa-md-6" rounded>
                        <h2 class="account__window-title title title_h2 title_black">
                            Заявки
                        </h2>
                        <request-table></request-table>
                    </v-sheet>
                </v-container>
            </v-window-item>
            <v-window-item class="account__window-item" :value="2">
                <v-container class="account__window-container" fluid>
                    <v-sheet class="account__window-sheet pa-4 pa-md-6" rounded>
                        <h2 class="account__window-title title title_h2 title_black">
                            Карты/счета
                        </h2>
                        <account-table></account-table>
                    </v-sheet>
                </v-container>
            </v-window-item>
            <v-window-item class="account__window-item" :value="3">
                <v-container class="account__window-container" fluid>
                    <v-sheet class="account__window-sheet pa-4 pa-md-6" rounded>
                        <account-form></account-form>
                    </v-sheet>
                </v-container>
            </v-window-item>
        </v-window>
    </div>
</template>

<script>
import {defineComponent, defineAsyncComponent} from 'vue';

export default defineComponent({
    name: 'AccountView',

    data: () => ({
        tab: 1,
        user: {
            oldPass: '',
            newPass: '',
            confirmPass: '',
        }
    }),
    components: {
        AccountForm: defineAsyncComponent({
            loader: () => import("../Forms/AccountForm"),
        }),
        RequestTable: defineAsyncComponent({
            loader: () => import("../Tables/RequestTable"),
        }),
        AccountTable: defineAsyncComponent({
            loader: () => import("../Tables/AccountTable"),
        }),
    },
    methods: {
        async changePassword() {
            let body = {
                "old_pass": this.user.oldPass,
                "new_pass" : this.user.newPass,
            }
            let response = await fetch('/api/lk/pass_change', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'accept':  'application/json',
                },
                body: JSON.stringify(body),
            });
            console.log(response);
        }
    }
});
</script>