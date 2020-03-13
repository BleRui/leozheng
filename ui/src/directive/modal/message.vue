<template>
    <div id="message">
        <Modal class="cw-message-modal"
               v-model="modalShow"
               width="320"
               v-if="style===1"
               :mask-closable="false">
            <div class="margin-top10 text-center">
                <div class="cw-modal-title">
                    <span v-if="type==='info'" class="font-bold">{{title}}</span>
                    <Icon type="md-checkmark-circle"
                          color="#5BD18B" size="46"
                          v-if="type==='success'"/>
                    <Icon type="md-alert"
                          color="#FEA30D" size="46"
                          v-if="type==='warning'"/>
                    <Icon type="md-close-circle"
                          color="#ED3F3F" size="46"
                          v-if="type==='error'"/>
                </div>
                <div class="margin-top15">{{content}}</div>
                <div class="margin-top20">
                    <Button type="primary"
                            @click="closeModal()"
                            v-if="type==='info'">
                        {{okText}}
                    </Button>
                    <Button @click="closeModal()"
                            v-if="type!=='info'">
                        {{okText}}
                    </Button>
                </div>
            </div>
        </Modal>
        <Modal class="cw-message-modal1" v-model="modalShow"
               :title="title"
               width="320" v-if="style===2" :mask-closable="false">
            <div class="margin-top10">
                <div class="font-18">
                    <Icon type="md-checkmark-circle"
                          color="#5BD18B" size="24"
                          v-if="type==='success'"/>
                    <Icon type="md-close-circle"
                          color="#ED3F3F" size="24"
                          v-if="type==='error'"/>
                    {{content}}
                </div>
                <div class="margin-top25 text-center">
                    <Button type="primary" @click="closeModal()">{{okText}}</Button>
                </div>
            </div>
        </Modal>
        <Modal class="cw-message-modal2" v-model="modalShow"
               :title="title"
               width="360" v-if="style===3">
            <div class="font-18" slot="header">
                <Icon type="md-checkmark-circle"
                      color="#5BD18B" size="24"
                      v-if="type==='success'"/>
                <Icon type="md-close-circle"
                      color="#ED3F3F" size="24"
                      v-if="type==='error'"/>
                {{content}}
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
         * @param {string} type 弹出框类型 可选值有：'success'、'warning'、'info'、'error'
         * @param {number} style 弹出框样式 可选值有：1, 2, 3, 不传默认为 1
         * @param {number} time 弹出框存在时间(单位：秒),只在 style 为 3 的情况下生效
         * @param {string} okText 确认按钮文字内容
         * @param {string} cancelText 取消按钮文字内容
         */
        name: 'message',
        data() {
            return {
                modalShow: false,
                title: '欢迎',
                content: '欢迎使用普通对话弹窗',
                time: 12000,
                type: 'info',
                okText: '确定',
                cancelText: '取消',
                style: 1
            }
        },
        mounted() {
            if (this.style === 3) this.close();
        },
        methods: {
            close() {
                window.setTimeout(() => {
                    this.modalShow = false
                }, this.time);
            },
            closeModal() {
                this.modalShow = false;
            }
        },
    }
</script>

<style scoped>
</style>
