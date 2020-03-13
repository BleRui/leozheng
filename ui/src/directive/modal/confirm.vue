<template>
    <div id="confirm">
        <Modal class="cw-message-modal"
               v-model="modalShow"
               width="320"
               :mask-closable="false">
            <div class="margin-top20 text-center">
                <div class="cw-modal-title">
                    <span>{{title}}</span>
                </div>
                <div class="margin-top10">{{content}}</div>
                <div class="margin-top25 margin-bottom10">
                    <Button type="primary"
                            @click="handleAction('yes')"
                            v-if="type==='edit'">
                        {{okText}}
                    </Button>
                    <Button type="error"
                            @click="handleAction('yes')"
                            v-if="type==='del'">
                        {{okText}}
                    </Button>
                    <Button class="margin-left10" @click="handleAction()">{{cancelText}}</Button>
                </div>
            </div>
        </Modal>
    </div>
</template>

<script>
    export default {
        /**
         * 参考: https://www.iviewui.com/components/modal
         * @param {string|number} title 弹框标题
         * @param {string|number} content 弹框内容
         * @param {string} type 弹出框类型 可选值有：'edit'、'del'
         * @param {string} okText 确认按钮文字内容
         * @param {string} cancelText 取消按钮文字内容
         * @param promiseStatus 构造promise函数，释放两个出口
         */
        name: 'confirm',
        data() {
            return {
                modalShow: false,
                title: '欢迎',
                content: '欢迎使用普通对话弹窗',
                type: 'edit',
                okText: '确定',
                cancelText: '取消',
                promiseStatus: null,
            }
        },
        mounted() {
        },
        methods: {
            confirm() {
                let _this = this;
                this.modalShow = true;
                return new Promise(function (resolve, reject) {
                    _this.promiseStatus = {resolve, reject};
                });
            },
            handleAction(action) {
                this.modalShow = false;
                if (action === 'yes') {
                    this.promiseStatus && this.promiseStatus.resolve();
                } else {
                    this.promiseStatus && this.promiseStatus.reject();
                }
            }
        },
    }
</script>

<style scoped>

</style>
