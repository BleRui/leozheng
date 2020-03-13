<template>
    <div id="jsoneditor" v-show="JsonData.is_show">
        <vue-json-editor class="jsondata" v-model="JsonData.data"
                         @json-change="onJsonChange" @json-save="AddJson"></vue-json-editor>
        <Button style="margin-left: 50%" type="info" @click="AddJson">保存</Button>
    </div>
</template>

<script>
    import vueJsonEditor from 'vue-json-editor'

    export default {
        name: 'json-editor',
        props: {
            JsonData: {
                is_show: false,
                data: {} //最好是Json格式
            }
        },
        mounted() {
            this.InitData()
        },
        data() {
            return {
                nowJsonData: {},
            }
        },
        // 注入vueJsonEditor组件
        components: {
            vueJsonEditor
        },
        methods: {
            //里面的值改变
            onJsonChange(value) {
                this.nowJsonData = value
            },
            AddJson() {
                console.log(this.nowJsonData)
            },
            InitData() {
                this.nowJsonData = this.JsonData.data
            }
        }
    }
</script>

<style lang='scss' scoped>
    #jsoneditor {
        width: 100%;
        height: 300px;
    }
</style>
<style lang="scss">
    .jsoneditor-menu { //顶部
        background-color: #097b9dba !important; //更改顶部框颜色
        color: #ffffff !important;
    }

    .jsoneditor-outer {
        height: 280px !important; //更改内容框大小
    }

    div.jsoneditor {
        border: none !important;//border框
        color: #ffffff !important;
    }

    jsoneditor-type-modes {
        color: #ffffff !important;
    }
</style>
