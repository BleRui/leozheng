// initial state
const state = {
    all: [1, 2, 3, 4]
}

// getters
const getters = {
    allData: () => {
        return state.all
    }
}

// mutations
const mutations = {
    setProducts(state, products) {
        state.all = products
    }
}

// actions
const actions = {
    setAllProducts({commit}) {
        commit('setProducts', [111, 3, 33, 444])
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}
