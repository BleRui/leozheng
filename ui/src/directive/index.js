import message from './modal/message'
import confirm from './modal/confirm'

//统一处理，
const methods = [
    message,
    confirm,
];

const install = function (Vue) {
    Vue.prototype.$CWConfirm = confirm.install;
    Vue.prototype.$CWMessage = message.install;
};

export default install;
