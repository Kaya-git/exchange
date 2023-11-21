import Vuex from 'vuex';

export default new Vuex.Store({
    state: {
      exchangeData: null,
    },
    mutations: {
      setExchangeData(state, data) {
        state.exchangeData = data;
      }
    },
    getters: {
      getExchangeData: state => state.exchangeData
    }
});