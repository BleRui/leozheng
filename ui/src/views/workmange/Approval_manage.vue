<template>
    <div>
        <Header>
        </Header>
        <Content>
            <Table height="350" border :columns="columns" :data="data" style="width: 100%">
                <template slot-scope="{ row, index }" slot="action">
                    <Button type="primary" size="small" style="margin-right: 5px" @click="details(row)">详情</Button>
                    <Button type="error" size="small" style="margin-right: 5px" @click="refuse(row)">拒绝</Button>
                    <Button type="success" size="small" style="margin-right: 5px" @click="pass(row)">通过</Button>
                </template>
            </Table>
            <Modal scrollable title="查看详情"
                   v-model="details_status"
                   @on-visible-change="calbac_shutdown">
                <!--详情-->
                <List border size="large">
                    <ListItem>工单标题：{{details_show.Job_title}}</ListItem>
                    <ListItem>工单内容：{{details_show.Job_content}}</ListItem>
                    <ListItem>执行主机：{{details_show.Execution_host}}</ListItem>
                    <ListItem>脚本内容：{{details_show.Script_content}}</ListItem>
                </List>
                <div slot="footer">
                    <Button @click="details_pass()" size="small" type="primary" ghost>通过</Button>
                    <Button @click="details_refuse('refused')" size="small" type="error" ghost>拒绝</Button>
                    <Button @click="cancel()" size="small" type="primary" ghost>取消</Button>
                </div>
            </Modal>
            <Modal scrollable title="拒绝理由"
                   loading="loading"
                   v-model="refused.reasons_status">
                <Form ref="refused" :model="refused" label-position="left" :rules="ruleInline" :label-width="100">
                    <FormItem label="拒绝理由" prop="reasons">
                        <Input v-model="refused.reasons"
                               type="textarea"
                               :autosize="{minRows: 2,maxRows: 6}"
                               placeholder="Enter reasons..."></Input>
                    </FormItem>
                </Form>
                <div slot="footer">
                    <Button @click="refuse_confirm('refused')" size="small" type="primary" ghost>确定</Button>
                    <Button @click="cancel()" size="small" type="primary" ghost>取消</Button>
                </div>
            </Modal>
        </Content>
    </div>
</template>

<script>
    export default {
        name: 'Approval_manage',
        data() {
            return {
                columns: [
                    {
                        title: '工单标题',
                        key: 'Job_title'
                    },
                    {
                        title: '申请人',
                        key: 'Applicant'
                    },
                    {
                        title: '申请时间',
                        key: 'Application_time'
                    },
                    {
                        title: '操作',
                        slot: 'action'
                    },
                ],
                data: [],
                details_status: false,
                details_show: {
                    Job_title: '',
                    Job_content: '',
                    Execution_host: '',
                    Script_content: '',
                    id: '',
                },
                ruleInline: {
                    //表单检验
                    reasons: [
                        {required: true, message: '拒绝理由', trigger: 'blur'}
                    ],
                },
                refused: {
                    reasons_status: false,
                    reasons: '',
                    id: '',
                    Status: '',
                },
                loading: true
            }
        },
        created() {
            this.get_work_management()
        },
        methods: {
            get_work_management() {
                // 获取提交的工单信息
                this.$api.User.get_work_management().then(res => {
                    this.data = res.data_Approval_info
                })
            },
            pass(row) {
                //通过按钮
                this.details_show.Execution_host = row.Execution_host
                this.details_show.Script_content = row.Script_content
                this.pass_fun(row.id)
            },
            refuse(row) {
                //拒绝
                this.refused.reasons_status = true
                this.refused.id = row.id
            },
            refuse_confirm(name) {
                //拒绝_确定
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        this.refused.reasons_status = false
                        this.refuse_fun(this.refused.id)
                    } else {
                        this.loading = false;
                        setTimeout(() => {
                            this.$nextTick(() => {
                                this.loading = true;
                            });
                        }, 300)
                    }
                })
            },
            details(row) {
                //详情
                this.details_status = true
                this.details_show.Job_title = row.Job_title
                this.details_show.Job_content = row.Job_content
                this.details_show.Execution_host = row.Execution_host
                this.details_show.Script_content = row.Script_content
                this.details_show.id = row.id
            },
            details_pass() {
                this.pass_fun(this.details_show.id)
                this.calbac()
            },
            details_refuse(name) {
                //详情_拒绝
                this.refused.reasons_status = true
                this.refused.id = this.details_show.id
            },
            cancel() {
                //详情_取消
                this.calbac()
            },
            calbac() {
                //回调
                this.details_status = false
                this.refused.reasons_status = false
                this.$refs['refused'].resetFields()
                this.details_show = {
                    Job_title: '',
                    Job_content: '',
                    Execution_host: '',
                    Script_content: '',
                    id: '',
                }
            },
            calbac_shutdown(val) {
                //回调
                if (val == false) {
                    this.$refs['refused'].resetFields()
                }
            },
            pass_fun(id) {
                let params = {
                    id: id,
                    Execution_host: this.details_show.Execution_host,
                    Script_content: this.details_show.Script_content
                }
                this.$api.User.Approval_pass(params).then(res => {
                    this.success('已通过！')
                    this.get_work_management()
                    this.calbac()
                })
            },
            refuse_fun(id) {
                let params = {
                    id: id,
                    Status: '拒绝',
                    Refusal_reasons: this.refused.reasons
                }
                this.$api.User.refuse_fun(params).then(res => {
                    if (res.result) {
                        this.error('已拒绝！')
                        this.get_work_management()
                        this.calbac()
                    }
                })
            },
            success(val) {
                this.$Notice.success({
                    title: val
                });
            },
            error(val) {
                this.$Notice.error({
                    title: val
                });
            },
        },
    }
</script>

<style scoped>

</style>
