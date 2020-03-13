import Vue from 'vue'
import Message from './message.vue'

const MessageBox = Vue.extend(Message);

Message.install = function (options) {
    let instance = new MessageBox({
        data: options
    }).$mount();

    document.body.appendChild(instance.$el); // 把生成的提示的dom插入body中

    Vue.nextTick(() => {
        instance.style = instance.style === undefined ? 1 : instance.style;
        instance.modalShow = true //显示提示组件
    })
};

export default Message
