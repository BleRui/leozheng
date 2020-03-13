// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import iViewUI from 'iview';
import 'jquery'
import axios from 'axios'
import 'iview/dist/styles/iview.css';
// 几何图
import Echarts from 'echarts'
import G2 from '@antv/g2';
// 引用API文件
import api from './api/index'
//时间格式化插件
import moment from 'moment'
//filter统一引入
import './fiter/index.js';
//公共方法
import './controller/func/common.js';
// 统一样式引入
import './assets/index'
// 引入自定义方法
import Dire from './directive/index.js'
// 引入自定义组件
import Component from './components/index.js'
//vuex
import store from './store/index'

Vue.use(ElementUI);
Vue.use(iViewUI);
Vue.use(Echarts);
Vue.use(G2);
Vue.use(Dire);
Vue.use(Component);
Vue.prototype.$echarts = Echarts;
Vue.prototype.$G2 = G2;
Vue.prototype.$moment = moment;
// 将API方法绑定到全局
Vue.prototype.$http = axios;
Vue.prototype.$api = api;
const headTheme = 'light'; //选择 light 或 blue
Vue.prototype.headTheme = headTheme;


/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    data() {
        return {
            website: '我是全局变量',
        }
    },
    components: {App},
    template: '<App/>',
});
