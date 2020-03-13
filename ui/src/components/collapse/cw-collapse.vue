<template>
    <div>
        <h3 class="margin-bottom10">折叠面板</h3>
        <Collapse accordion :simple="hasTable">
            <Panel v-for="(item, index) in info" :key="index">
                {{item[props.title]}}
                <div slot="content" v-for="(child,c_index) in item[props.children]" :key="c_index" v-if="!hasTable">
                    <p class="padding-5">{{child[props.content]}}</p>
                </div>
                <div slot="content" v-if="hasTable">
                    <Table border :columns="columns[index]" :data="item[props.children]"
                           :style="{'max-height': 40 + 48 * item[props.children].length + 'px'}"></Table>
                </div>
            </Panel>
        </Collapse>
    </div>
</template>

<script>
    export default {
        /**
         * 面板内容以段落展示
         * 参考 https://www.iviewui.com/components/collapse
         * @params {objects list} info 面板的名称
         * @params {objects list} contents 面板的内容
         * @params {objects Boolean} hasTable 面板风格 是否展示table
         * @params {objects list} columns table的表头，在hasTable下生效
         * @params {objects} props 展示的数据key
         * */
        name: 'CWCollapse',
        props: {
            info: {
                default() {
                    return [
                        {
                            title: '第一条测试',
                            children: [
                                {
                                    content: '1111',
                                    name: 'C:',
                                    size: '99.68GB',
                                    left: '77.17GB',
                                    percentage: '77.14'
                                },
                                {
                                    content: '222',
                                    name: 'C:',
                                    size: '99.68GB',
                                    left: '77.17GB',
                                    percentage: '77.14'
                                },
                            ]
                        }, {
                            title: '第二条测试',
                            children: [
                                {
                                    content: '2111',
                                    place: 'pc-abcde',
                                    time: '2010-01-12',
                                    grade: 'high',
                                    people: 'Jason'
                                }
                            ]
                        }, {
                            title: '第三条测试',
                            children: [
                                {
                                    content: '3111',
                                    place: 'http://www.baidu.com',
                                    sum: '10',
                                    success: '10',
                                    result: 'none'
                                }
                            ]
                        }
                    ]
                }
            },
            props: {
                type: Object,
                default() {
                    return {
                        title: 'title',
                        children: 'children',
                        content: 'content'
                    }
                }
            },
            hasTable: {
                type: Boolean,
                default: false
            },
            columns: {
                default() {
                    return [
                        [
                            {
                                title: '分区名称',
                                key: 'name'
                            },
                            {
                                title: '分区大小',
                                key: 'size'
                            },
                            {
                                title: '剩余空间',
                                key: 'left'
                            },
                            {
                                title: '剩余空间比',
                                key: 'percentage'
                            }
                        ],
                        [
                            {
                                title: '故障位置',
                                key: 'place'
                            },
                            {
                                title: '故障时间',
                                key: 'time'
                            },
                            {
                                title: '故障级别',
                                key: 'grade'
                            },
                            {
                                title: '处理人',
                                key: 'people'
                            }
                        ], [
                            {
                                title: '请求地址',
                                key: 'place'
                            },
                            {
                                title: '请求次数',
                                key: 'sum'
                            },
                            {
                                title: '成功次数',
                                key: 'success'
                            },
                            {
                                title: '请求结果',
                                key: 'result'
                            }],
                    ]
                }
            }
        }
    }
</script>

<style scoped>
</style>
