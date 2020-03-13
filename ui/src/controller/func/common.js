import Vue from 'vue';
//loading显示
Vue.prototype.$showLoading = function () {
    this.$Spin.show({
        render: (h) => {
            return h('div', [
                h('Icon', {
                    'class': 'demo-spin-icon-load',
                    props: {
                        type: 'ios-loading',
                        size: 18
                    }
                }),
                h('div', 'Loading')
            ])
        }
    });
};
//loading关闭
Vue.prototype.$CloseLoading = function () {
    this.$Spin.hide();
};
//去重
Vue.prototype.$DupRem = function (list) {
    let newArr = [];
    for (var i = 0; i < list.length; i++) {
        if (newArr.indexOf(list[i]) < 0) {
            newArr.push(list[i])
        }
    }
    return newArr;
};
//深拷贝
Vue.prototype.$Copy = function (data) {
    return JSON.parse(JSON.stringify(data))
};

//时间格式转string
Vue.prototype.$TransTime = function (date) {
    let data = new Date(date)
    let sep = '-';
    let year = data.getFullYear();
    let month = data.getMonth() + 1;
    let strDate = data.getDate();
    if (month >= 1 && month <= 9) {
        month = '0' + month;
    }
    if (strDate >= 0 && strDate <= 9) {
        strDate = '0' + strDate;
    }
    return year + sep + month + sep + strDate;
}

//时间管理  days:时间间隔 startDate:初始时间 type:返回时间格式,默认返回string格式（string or time）
Vue.prototype.$DateDisplay = function (days, type, startDate) {
    const end = startDate ? new Date(startDate) : new Date();
    const start = startDate ? new Date(startDate) : new Date();
    end.setTime(start.getTime() + 24 * 60 * 60 * 1000);
    start.setTime(start.getTime() - 3600 * 1000 * 24 * days);
    return {
        endTime: type === 'time' ? end : Vue.prototype.$TransTime(end),
        startTime: type === 'time' ? start : Vue.prototype.$TransTime(start)
    }
}
