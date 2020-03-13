<template>
    <div id="transfer">
        <div class="cw-trans-left dis-inline">
            <div class="cw-trans-search" v-if="filterable">
                <Input search :placeholder="filterPlaceholder" v-model="leftSearch"/>
            </div>
            <div class="el-transfer-panel">
                <div class="el-transfer-panel__header cw-trans-header">
                    <div class="dis-inline">
                        <el-checkbox class="dis-inline"
                                     :indeterminate="leftIndeterminate"
                                     v-model="leftAll"
                                     @change="leftCheckAll">
                            <div class="dis-inline font-14">{{titles[0]}}</div>
                        </el-checkbox>
                    </div>
                </div>
                <div class="el-transfer-panel__body">
                    <el-checkbox-group
                        v-model="leftChecked"
                        v-if="sourceData.length!==0"
                        class="el-transfer-panel__list">
                        <el-checkbox v-for="item in sourceData"
                                     :key="item[props.key]"
                                     :label="item[props.key]"
                                     class="el-transfer-panel__item">
                            {{item[props.label]}}
                        </el-checkbox>
                    </el-checkbox-group>
                    <p class="el-transfer-panel__empty" v-if="sourceData.length===0">无数据</p>
                </div>
            </div>
        </div>
        <div class="cw-trans-middle margin-20">
            <button type="button" :class="{'ivu-btn-primary':leftChecked.length>0}"
                    class="ivu-btn ivu-btn-default margin-bottom10"
                    @click="changeTarget('left')">
                <i class="el-icon-d-arrow-right"></i>
            </button>
            <button type="button" :class="{'ivu-btn-primary':rightChecked.length>0}"
                    class="ivu-btn ivu-btn-default"
                    @click="changeTarget('right')">
                <i class="el-icon-d-arrow-left"></i>
            </button>
        </div>
        <div class="dis-inline">
            <div class="cw-trans-search" v-if="filterable">
                <Input search :placeholder="filterPlaceholder" v-model="rightSearch"/>
            </div>
            <div class="el-transfer-panel">
                <div class="el-transfer-panel__header cw-trans-header">
                    <div class="dis-inline">
                        <el-checkbox class="dis-inline"
                                     :indeterminate="rightIndeterminate"
                                     v-model="rightAll"
                                     @change="rightCheckAll">
                            <div class="dis-inline font-14">{{titles[1]}}</div>
                        </el-checkbox>
                    </div>
                    <div class="dis-inline cw-trans-act font-14" v-if="showDelete">
                        操作
                    </div>
                </div>
                <div class="el-transfer-panel__body">
                    <el-checkbox-group
                        v-if="targetData.length!==0"
                        v-model="rightChecked"
                        class="el-transfer-panel__list">
                        <el-checkbox v-for="item in targetData"
                                     :label="item[props.key]"
                                     :key="item[props.key]"
                                     class="el-transfer-panel__item">
                            <div class="dis-inline cw-trans-check-contain">
                                <span>{{item[props.label]}}</span>
                                <button type="button" class="ivu-btn ivu-btn-error ivu-btn-small ivu-btn-ghost"
                                        @click="deleteTarget(item)" v-if="showDelete">
                                    删除
                                </button>
                            </div>
                        </el-checkbox>
                    </el-checkbox-group>
                    <p class="el-transfer-panel__empty" v-if="targetData.length===0">无数据</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    /**
     * 参考: https://codemirror.net/
     * @param {List} value 右侧展示数据
     * @param {List} data 全部数据
     * @param {List} titles 左右两侧标题
     * @param {string} filterPlaceholder 搜索框占位
     * @param {Boolean} filterable 是否展示搜索框
     * @param {Boolean} showDelete 是否展示右侧删除按钮
     * @param {Object} props 自定义展示字段，key:唯一标识，label:展示和搜索字段，disabled:是否可被操作
     * 更多支持语言和风格请参考官方文档，引入即可
     * */
    export default {
        name: 'CWTransfer',
        props: {
            value: {
                type: Array,
                default() {
                    return [
                        {'key': 1, 'label': 'Content 1', 'disabled': false},
                        {'key': 2, 'label': 'Content 2', 'disabled': false},
                        {'key': 3, 'label': 'Content 3', 'disabled': false}
                    ];
                }
            },
            data: {
                type: Array,
                default() {
                    return [{'key': 1, 'label': 'Content 1', 'disabled': false},
                        {'key': 2, 'label': 'Content 2', 'disabled': false},
                        {'key': 3, 'label': 'Content 3', 'disabled': false},
                        {'key': 4, 'label': 'Content 4', 'disabled': false},
                        {'key': 5, 'label': 'Content 5', 'disabled': false},
                        {'key': 6, 'label': 'Content 6', 'disabled': false}];
                }
            },
            titles: {
                type: Array,
                default() {
                    return ['未选项', '已选项'];
                }
            },
            filterPlaceholder: {
                type: String,
                default: '请输入名称搜索'
            },
            filterable: {
                type: Boolean,
                default: true
            },
            showDelete: {
                type: Boolean,
                default: true
            },
            props: {
                type: Object,
                default() {
                    return {
                        label: 'label',
                        key: 'key',
                        disabled: 'disabled'
                    };
                }
            }
        },
        data() {
            return {
                selectData: this.value,
                leftAll: false,
                rightAll: false,
                leftChecked: [],
                leftIndeterminate: false,
                rightChecked: [],
                rightIndeterminate: false,
                valueData: this.value.map(item => item[this.props.key]),
                leftSearch: '',
                rightSearch: '',
            }
        },
        watch: {
            valueData() {
                this.selectData = this.data.filter(item => this.valueData.indexOf(item[this.props.key]) > -1)
                this.$emit('input', this.selectData);
            },
            leftChecked() {
                this.leftAll = this.sourceData.length > 0 ? this.leftChecked.length === this.sourceData.length : false
                this.leftIndeterminate = this.leftChecked.length > 0 && this.leftChecked.length < this.sourceData.length
            },
            rightChecked() {
                this.rightAll = this.targetData.length > 0 ? this.rightChecked.length === this.targetData.length : false
                this.rightIndeterminate = this.rightChecked.length > 0 && this.rightChecked.length < this.targetData.length
            },
            sourceData() {
                this.leftChecked = []
            },
            targetData() {
                this.rightChecked = []
            },
        },
        computed: {
            sourceData() {
                return this.data.filter(item => this.valueData.indexOf(item[this.props.key]) === -1 &&
                    item[this.props.label].indexOf(this.leftSearch) !== -1);
            },
            targetData() {
                return this.data.filter(item => this.valueData.indexOf(item[this.props.key]) > -1 &&
                    item[this.props.label].indexOf(this.rightSearch) !== -1);
            },
        },
        methods: {
            leftCheckAll(val) {
                this.leftChecked = val ? this.sourceData.map(item => item[this.props.key]) : [];
                this.leftIndeterminate = false;
            },
            rightCheckAll(val) {
                this.rightChecked = val ? this.targetData.map(item => item[this.props.key]) : [];
                this.rightIndeterminate = false;
            },
            deleteTarget(item) {
                this.valueData.splice(this.valueData.indexOf(item[this.props.key]), 1)
            },
            changeTarget(direct) {
                if (direct === 'left') {
                    this.valueData = this.valueData.concat(this.leftChecked)
                    this.leftChecked = []
                } else {
                    let list = this.$Copy(this.valueData)
                    this.rightChecked.forEach(item => {
                        list.splice(list.indexOf(item), 1)
                    })
                    this.valueData = list
                    this.rightChecked = []
                }
            }
        }
    }
</script>

<style>
    .cw-trans-search {
        width: 200px;
        margin-bottom: 5px;
    }

    .cw-trans-header {
        display: flex;
        justify-content: space-between;
    }

    .cw-trans-act {
        padding: 0 20px;
        border-left: 1px solid #e8eaec;
    }

    .cw-trans-check-contain {
        display: flex;
        justify-content: space-between;
        align-items: center
    }

    .cw-trans-middle {
        display: inline-flex;
        flex-direction: column;
        position: relative;
        top: -50px;
    }
</style>
