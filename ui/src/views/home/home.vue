<template>
    <div id='home'>
        <div class="padding-top10" style="height: 100%;">
            <Row>
                <Col span="2" class="padding-left10">
                    <ButtonGroup class="CW-group-ghost" vertical size="large">
                        <Button type="info" ghost
                                v-for="item in comList"
                                :key="item.file"
                                @click="changeType(item.file)">
                            {{item.name}}
                        </Button>
                    </ButtonGroup>
                </Col>
                <Col span="22" class="right-box">
                    <transition name="component-trans" mode="out-in">
                        <component :is="comType" v-if="comType!=='chart' & comType !=='CWCollapse2'"></component>
                        <div v-else-if="comType ==='CWCollapse2'">
                            <CWCollapse hasTable></CWCollapse>
                        </div>
                        <div id="panChartLeft" v-else :style="{width: '100%', height: '350px'}"></div>
                    </transition>
                </Col>
            </Row>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'home',
        data() {
            return {
                comType: 'Buttons',
                comList: [
                    {name: '按钮', file: 'Buttons'},
                    {name: '选项卡', file: 'CWView'},
                    {name: '表单', file: 'iViewTwo'},
                    {name: '穿梭框', file: 'CWTransfer'},
                    {name: '折叠面板1', file: 'CWCollapse'},
                    {name: '折叠面板2', file: 'CWCollapse2'},
                    {name: '图表', file: 'chart'}
                ]
            }
        },
        watch: {
            comType() {
                if (this.comType === 'chart') {
                    setTimeout(() => {
                        this.drawLeft()
                    }, 300)
                }
            }
        },
        methods: {
            getData() {
                this.$api.User.homeInfo().then(res => {
                });
            },
            drawLeft() {
                //柱形图
                let panChartLeft = this.$echarts.init(document.getElementById('panChartLeft'));
                panChartLeft.setOption({
                    xAxis: {
                        type: 'category',
                        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
                    },
                    yAxis: {
                        type: 'value'
                    },
                    series: [{
                        data: [820, 932, 901, 934, 1290, 1330, 1320],
                        type: 'line'
                    }]
                });
            },
            changeType(data) {
                this.comType = data
            }
        }
    }
</script>

<style scoped lang='scss'>
    #home {
        height: 100%;
        width: 100%;
        padding: 10px;

        .right-box {
            padding: 10px 20px;
            border: 2px solid $primary-color;
        }
        .component-trans-enter-active, .component-trans-leave-active {
            transition: opacity .25s ease;
        }
        .component-trans-enter, .component-trans-leave-to {
            opacity: 0;
        }
    }
</style>
