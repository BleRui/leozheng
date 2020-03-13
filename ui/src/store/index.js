import Vuex from 'vuex'
import Vue from 'vue'
import product from './modules/product'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {product}
})
