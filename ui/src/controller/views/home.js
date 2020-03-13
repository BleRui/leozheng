export default {
        name: 'home',
        data() {
            return {
                service: {},
                lists: [
                    {
                        name: '驴打1',
                        disable: false,
                    },
                    {
                        name: '炸酱2',
                        disable: false,
                    },
                    {
                        name: '冰糖葫3',
                        disable: false,
                    },
                    {
                        name: '北京烤4',
                        disable: false,
                    },
                ],
                showPage: true,
            }
        },
        mounted() {
            // this.getData();
            // this.$showLoading();
        },
        methods: {
            getData() {
                this.$api.Server.homeInfo().then(res => {
                });
            },
            drawLeft(data) {
                //柱形图
                let panChartLeft = this.$echarts.init(document.getElementById('panChartLeft'));
                panChartLeft.setOption({
                    title: {
                        text: '服务使用频率Top5',
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {show: true},
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    calculable: true,
                    xAxis: [
                        {
                            type: 'category',
                            data: data.x_data
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: '使用次数',
                            type: 'bar',
                            color: '#709ed8',
                            data: data.y_data,
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                        }
                    ]
                });
            },
            drawRight(data) {
                let panChartRight = this.$echarts.init(document.getElementById('panChartRight'));
                panChartRight.setOption({
                    title: {
                        text: '服务申请频率Top5',
                    },
                    tooltip: {
                        trigger: 'axis'
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            mark: {show: true},
                            dataView: {show: true, readOnly: false},
                            magicType: {show: true, type: ['line', 'bar']},
                            restore: {show: true},
                            saveAsImage: {show: true}
                        }
                    },
                    calculable: true,
                    xAxis: [
                        {
                            type: 'category',
                            data: data.x_data
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value'
                        }
                    ],
                    series: [
                        {
                            name: '申请次数',
                            type: 'bar',
                            color: '#64a9ff',
                            data: data.y_data,
                            markPoint: {
                                data: [
                                    {type: 'max', name: '最大值'},
                                    {type: 'min', name: '最小值'}
                                ]
                            },
                            markLine: {
                                data: [
                                    {type: 'average', name: '平均值'}
                                ]
                            }
                        }
                    ]
                });
            }
        }
    }
