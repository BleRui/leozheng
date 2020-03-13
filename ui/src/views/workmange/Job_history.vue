<template>
    <div>
        <Header>
        </Header>
        <Content>
            <Table height="350" border :columns="columns" :data="data" style="width: 100%">
                <template slot-scope="{ row, index }" slot="action">
                    <div v-if="row.State=='拒绝'">
                        <Button type="primary" size="small" style="margin-right: 5px" @click="see_fun(row)">查看</Button>
                        <Button type="success" size="small" @click="modify(row)">修改</Button>
                    </div>
                    <div v-else>
                        <Button type="primary" size="small" @click="see_fun(row)">查看</Button>
                    </div>
                </template>
            </Table>
            <Modal draggable scrollable title="查看详情"
                   v-model="see.status"
                   @on-visible-change="calbac_shutdown">
                <!--详情-->
                <List border size="large">
                    <ListItem>工单标题：{{see.Job_title}}</ListItem>
                    <ListItem>工单内容：{{see.Job_content}}</ListItem>
                    <ListItem>执行主机：{{see.Execution_host}}</ListItem>
                    <ListItem>脚本内容：{{see.Script_content}}</ListItem>
                    <ListItem v-if="see.rowStatus=='拒绝'">拒绝理由：{{see.Refusal_reasons}}</ListItem>
                    <ListItem v-else>脚本结果：{{see.ScriptResults}}</ListItem>
                </List>
                <div slot="footer">
                    <Button @click="cancel()" type="primary" ghost>关闭</Button>
                </div>

            </Modal>
            <Modal title="修改工单"
                   v-model="modify_data.show"
                   :loading="modify_data.loading">
                <!--修改工单表格-->
                <Form ref="modify_data" :model="modify_data" label-position="left" :rules="ruleInline"
                      :label-width="100">
                    <FormItem label="工单标题" prop="Job_title_input">
                        <Input v-model="modify_data.Job_title_input"></Input>
                    </FormItem>
                    <FormItem label="工单内容" prop="Job_content_input">
                        <Input v-model="modify_data.Job_content_input"></Input>
                    </FormItem>
                    <FormItem label="执行主机" prop="Execution_host_select">
                        <Select v-model="modify_data.Execution_host_select" style="width:200px">
                            <Option v-for="item in hostList" :value="item.bk_host_innerip" :key="item.bk_host_innerip">
                                {{ item.bk_host_innerip }}
                            </Option>
                        </Select>
                    </FormItem>
                    <FormItem label="脚本内容" prop="Script_content_input">
                        <Input v-model="modify_data.Script_content_input"
                               type="textarea"
                               :autosize="{minRows: 2,maxRows: 5}"
                               placeholder="Enter Script content..."></Input>
                    </FormItem>
                    <FormItem label="审批人" prop="Approver_select">
                        <Select @on-change="perChange" v-model="modify_data.Approver_select"
                                label-in-value="true"
                                style="width:200px">
                            <Option v-for="item in ApproverList" :value="item.bk_username"
                                    :key="item.bk_username">{{ item.display_name }}
                            </Option>
                        </Select>
                    </FormItem>
                </Form>
                <div slot="footer">
                    <Button @click="modify_save('modify_data')" type="primary" ghost>保存</Button>
                    <Button @click="modify_submit('modify_data')" type="primary" ghost>提交</Button>
                    <Button @click="cancel()" type="primary" ghost>取消</Button>
                </div>
            </Modal>
        </Content>
    </div>
</template>

<script>
    export default {
        name: 'Job_history',
        data() {
            return {
                columns: [
                    {
                        title: '工单标题',
                        key: 'Job_title'
                    },
                    {
                        title: '执行主机',
                        key: 'Execution_host'
                    },
                    {
                        title: '申请人',
                        key: 'Applicant'
                    },
                    {
                        title: '审批人',
                        key: 'Approver'
                    },
                    {
                        title: '状态 ',
                        key: 'State'
                    },
                    {
                        title: '操作',
                        slot: 'action'
                    },
                ],
                data: [],
                hostList: [],
                ApproverList: [],
                ruleInline: {
                    //表单检验
                    Job_title_input: [
                        {required: true, message: '工单标题', trigger: 'blur'}
                    ],
                    Job_content_input: [
                        {required: true, message: '工单内容', trigger: 'blur'}
                    ],
                    Execution_host_select: [
                        {required: true, message: '执行主机', trigger: 'blur'}
                    ],
                    Script_content_input: [
                        {required: true, message: '脚本内容', trigger: 'blur'}
                    ],
                    Approver_select: [
                        {required: true, message: '审批人', trigger: 'blur'}
                    ],
                },
                see: {
                    rowStatus: '',
                    status: false,
                    Job_title: '',
                    Job_content: '',
                    Execution_host: '',
                    Script_content: '',
                    ScriptResults: '',
                    Refusal_reasons: '',
                    id: '',
                },
                modify_data: {
                    show: false,
                    loading: true,
                    Job_title_input: '',
                    Job_content_input: '',
                    Execution_host_select: '',
                    Script_content_input: '',
                    Approver_select: '',
                    Approver_display: '',
                },
            }
        },
        created() {
            this.get_work_management()
        },
        methods: {
            get_work_management() {
                // 获取提交的工单信息
                this.$api.User.get_work_management().then(res => {
                    this.data = res.data_history_info
                })
            },
            see_fun(row) {
                //查看
                this.see.status = true
                this.see.Job_title = row.Job_title
                this.see.Job_content = row.Job_content
                this.see.Execution_host = row.Execution_host
                this.see.Script_content = row.Script_content
                this.see.ScriptResults = row.ScriptResults
                this.see.rowStatus = row.State
                this.see.Refusal_reasons = row.Refusal_reasons
                this.see.id = row.id
            },
            modify(row) {
                // 修改
                this.get_host();
                this.get_allUser();
                this.modify_data.show = true
                this.modify_data.Job_title_input = row.Job_title
                this.modify_data.Job_content_input = row.Job_content
                this.modify_data.Execution_host_select = row.Execution_host
                this.modify_data.Script_content_input = row.Script_content
                this.modify_data.Approver_select = row.Approver
                this.modify_data.Approver_display = row.Approver_display
                this.modify_data.id = row.id
            },
            modify_save(name) {
                //修改_保存按钮
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            Job_title: this.modify_data.Job_title_input,
                            Job_content: this.modify_data.Job_content_input,
                            Execution_host: this.modify_data.Execution_host_select,
                            Script_content: this.modify_data.Script_content_input,
                            Approver: this.modify_data.Approver_select,
                            Approver_display: this.modify_data.Approver_display,
                            id: this.modify_data.id
                        };
                        this.$api.User.add_save_wm(params).then(res => {
                            if (res.result) {
                                this.delete_work_info1(this.modify_data.id)
                                this.success('保存成功！')
                                this.get_work_management()
                                this.cancel()
                            }
                        })
                    } else {
                        this.modify.loading = false;
                        setTimeout(() => {
                            this.$nextTick(() => {
                                this.modify.loading = true;
                            });
                        }, 300)
                        this.loading = false
                    }
                })
            },
            modify_submit(name) {
                //修改_提交
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            Job_title: this.modify_data.Job_title_input,
                            Job_content: this.modify_data.Job_content_input,
                            Execution_host: this.modify_data.Execution_host_select,
                            Script_content: this.modify_data.Script_content_input,
                            Approver: this.modify_data.Approver_select,
                            Approver_display: this.modify_data.Approver_display,
                        }
                        this.$api.User.add_submit(params).then(res => {
                            if (res.result) {
                                this.delete_work_info1(this.modify_data.id)
                                this.success('提交成功！')
                                this.get_work_management()
                                this.cancel()
                            }
                        })
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
            get_host() {
                // 获取所有主机
                this.$api.User.get_allHost_ip().then(res => {
                    this.hostList = res.data
                })
            },
            get_allUser() {
                // 获取所有用户
                this.$api.User.get_allUser().then(res => {
                    this.ApproverList = res.data
                })
            },
            delete_work_info1(id) {
                let params = {
                    id: id
                }
                this.$api.User.delete_work_info(params).then(res => {
                    if (res.result) {
                        console.log('1')
                    }
                })
            },
            perChange(e) {
                //触发选择审批人
                this.formLeft.Approver_select = e.value
                this.formLeft.Approver_display = e.label
            },
            cancel() {
                this.see = {
                    rowStatus: '',
                    status: false,
                    Job_title: '',
                    Job_content: '',
                    Execution_host: '',
                    Script_content: '',
                    ScriptResults: '',
                    Refusal_reasons: '',
                    id: '',
                }
                this.modify_data.show = false
                this.$refs['modify_data'].resetFields()
            },
            calbac_shutdown(val) {
                //回调
                if (val == false) {
                    this.see = {
                        rowStatus: '',
                        status: false,
                        Job_title: '',
                        Job_content: '',
                        Execution_host: '',
                        Script_content: '',
                        ScriptResults: '',
                        Refusal_reasons: '',
                        id: '',
                    }
                }
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
