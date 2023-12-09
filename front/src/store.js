import Vuex from 'vuex';

export default new Vuex.Store({
    state: {
      exchangeData: null,
      verificationFile: null,
      waitOverlay: false,
      confirmOverlay: false,
      requestFixedTime: 15,
      timer: false,
    },
    mutations: {
      setExchangeData(state, data) {
        state.exchangeData = data;
      },
      setVerificationFile(state, data) {
        state.verificationFile = data;
      },
      openWaitOverlay(state) {
        state.waitOverlay = true;
      },
      closeWaitOverlay(state) {
        state.waitOverlay = false;
      },
      toggleWaitOverlay(state) {
        state.waitOverlay = !state.waitOverlay;
      },
      openConfirmOverlay(state) {
        state.confirmOverlay = true;
      },
      closeConfirmOverlay(state) {
        state.confirmOverlay = false;
      },
      toggleConfirmOverlay(state) {
        state.confirmOverlay = !state.confirmOverlay;
      }
    },
    actions: {
      async startCounter({ state }) {
        state.timer = true;
        while (state.requestFixedTime > 0 && state.timer) {
          await new Promise(resolve => setTimeout(resolve, 1000));
          if (state.timer)
            state.requestFixedTime--;
        }
        state.timer = false;
      },
      resetRequestTime({ state }) {
        state.requestFixedTime = 15;
        state.timer = false;
      }
    },
    getters: {
      getExchangeData: state => state.exchangeData,
      getVerificationFile: state => state.verificationFile,
      getWaitOverlayState: state => state.waitOverlay,
      getConfirmOverlayState: state => state.confirmOverlay,
      getRequestFixedTime: state => state.requestFixedTime,
    }
});