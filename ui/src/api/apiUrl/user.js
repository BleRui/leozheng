// 获取登录信息！！！勿动
import {get, post, reUrl} from '../axiosconfig/axiosconfig'

// 返回在vue模板中的调用接口
export default {
    //----GET-------------------------------------------------------------
    //获取登录信息！！！
    homeInfo: function (params) {
        return get(reUrl + '/login_info', params)
    },
    get_allHost_ip: function (params) {
        return post(reUrl + '/get_allHost_ip', params)
    },
    get_allUser: function (params) {
        return post(reUrl + '/get_allUser', params)
    },
    get_work_management: function (params) {
        return post(reUrl + '/get_work_management', params)
    },
    add_save_wm: function (params) {
        return post(reUrl + '/add_save_wm', params)
    },
    delete_work_management: function (params) {
        return post(reUrl + '/delete_work_management', params)
    },
    modify_save_wm: function (params) {
        return post(reUrl + '/modify_save_wm', params)
    },
    submit: function (params) {
        return post(reUrl + '/submit', params)
    },
    Approval_pass: function (params) {
        return post(reUrl + '/Approval_pass', params)
    },
    add_submit: function (params) {
        return post(reUrl + '/add_submit', params)
    },
    refuse_fun: function (params) {
        return post(reUrl + '/refuse_fun', params)
    },
    delete_work_info: function (params) {
        return post(reUrl + '/delete_work_info', params)
    },
}
