<template>
    <div>
        <Header>
            <Row type="flex" align="middle" class="code-row-bg">
                <Col span="12" push="20" class="grid-content bg-purple">
                    <Button type="primary" size="mini"
                            @click="add_status = true,modal_load=true,add_work_management()">添加工单
                    </Button>
                </Col>
            </Row>
        </Header>
        <Content>
            <Table height="350" border :columns="columns" :data="data" style="width: 100%">
                <template slot-scope="{ row, index }" slot="action">
                    <Button type="primary" size="small" style="margin-right: 5px"
                            @click="modify_status = true,modify_work_management(row)">修改
                    </Button>
                    <Button type="primary" size="small" style="margin-right: 5px" @click="submit(row)">提交
                    </Button>
                    <Button type="error" size="small" @click="delete_work_management(row)">删除</Button>
                </template>
            </Table>
            <Modal title="添加工单"
                   v-model="add_status"
                   :loading="loading">
                <!--添加工单表单-->
                <Form ref="formLeft" :model="formLeft" label-position="left" :rules="ruleInline" :label-width="100">
                    <FormItem label="工单标题" prop="Job_title_input">
                        <Input v-model="formLeft.Job_title_input"></Input>
                    </FormItem>
                    <FormItem label="工单内容" prop="Job_content_input">
                        <Input v-model="formLeft.Job_content_input"></Input>
                    </FormItem>
                    <FormItem label="执行主机" prop="Execution_host_select">
                        <Select v-model="formLeft.Execution_host_select" style="width:200px">
                            <Option v-for="item in hostList" :value="item.bk_host_innerip" :key="item.bk_host_innerip">
                                {{ item.bk_host_innerip }}
                            </Option>
                        </Select>
                    </FormItem>
                    <FormItem label="脚本内容" prop="Script_content_input">
                        <Input v-model="formLeft.Script_content_input"
                               type="textarea"
                               :autosize="{minRows: 2,maxRows: 5}"
                               placeholder="Enter something..."></Input>
                    </FormItem>
                    <FormItem label="审批人" prop="Approver_select">
                        <Select @on-change="perChange" v-model="formLeft.Approver_select"
                                label-in-value="true"
                                style="width:200px">
                            <Option v-for="item in ApproverList" :value="item.bk_username"
                                    :key="item.bk_username">{{ item.display_name }}
                            </Option>
                        </Select>
                    </FormItem>
                </Form>
                <div slot="footer">
                    <Button @click="add_save_wm('formLeft')" type="primary" ghost>保存</Button>
                    <Button @click="add_submit('formLeft')" type="primary" ghost>提交</Button>
                    <Button @click="calbac()" type="warning" ghost>取消</Button>
                </div>
            </Modal>
            <Modal title="修改工单"
                   v-model="modify_status"
                   :loading="loading_modify">
                <!--修改工单表格-->
                <Form ref="oldData" :model="oldData" label-position="left" :rules="ruleInline" :label-width="100">
                    <FormItem label="工单标题" prop="Job_title_input">
                        <Input v-model="oldData.Job_title_input"></Input>
                    </FormItem>
                    <FormItem label="工单内容" prop="Job_content_input">
                        <Input v-model="oldData.Job_content_input"></Input>
                    </FormItem>
                    <FormItem label="执行主机" prop="Execution_host_select">
                        <Select v-model="oldData.Execution_host_select" style="width:200px">
                            <Option v-for="item in hostList" :value="item.bk_host_innerip" :key="item.bk_host_innerip">
                                {{ item.bk_host_innerip }}
                            </Option>
                        </Select>
                    </FormItem>
                    <FormItem label="脚本内容" prop="Script_content_input">
                        <Input v-model="oldData.Script_content_input"
                               type="textarea"
                               :autosize="{minRows: 2,maxRows: 5}"
                               placeholder="Enter Script content..."></Input>
                    </FormItem>
                    <FormItem label="审批人" prop="Approver_select">
                        <Select @on-change="perChange" v-model="oldData.Approver_select"
                                label-in-value="true"
                                style="width:200px">
                            <Option v-for="item in ApproverList" :value="item.bk_username"
                                    :key="item.bk_username">{{ item.display_name }}
                            </Option>
                        </Select>
                    </FormItem>
                </Form>
                <div slot="footer">
                    <Button @click="modify_save_wm('oldData')" type="primary" ghost>保存</Button>
                    <Button @click="calbac()" type="warning" ghost>取消</Button>
                </div>
            </Modal>
        </Content>
    </div>
</template>

<script>
    export default {
        name: 'workmanage',
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
                        title: '操作',
                        slot: 'action'
                    },
                ],
                data: [],
                formLeft: {
                    Job_title_input: '',
                    Job_content_input: '',
                    Execution_host_select: '',
                    Script_content_input: '',
                    Approver_select: '',
                    Approver_display: '',
                },
                oldData: {
                    Job_title_input: '',
                    Job_content_input: '',
                    Execution_host_select: '',
                    Script_content_input: '',
                    Approver_select: '',
                    Approver_display: '',
                },
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
                hostList: [],
                ApproverList: [],
                add_status: false,
                modify_status: false,
                loading: true,
                loading_modify: true,
            }
        },
        created() {
            // this.myFunc()
            this.get_work_management()
        },
        methods: {
            add_work_management() {
                // 添加工单按钮
                this.get_host()
                this.get_allUser()
            },
            add_save_wm(name) {
                // 添加工单_确定按钮
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            Job_title: this.formLeft.Job_title_input,
                            Job_content: this.formLeft.Job_content_input,
                            Execution_host: this.formLeft.Execution_host_select,
                            Script_content: this.formLeft.Script_content_input,
                            Approver: this.formLeft.Approver_select,
                            Approver_display: this.formLeft.Approver_display,
                        }
                        this.$api.User.add_save_wm(params).then(res => {
                            if (res.result) {
                                this.success('添加成功！')
                                this.get_work_management()
                                this.calbac()
                                this.add_status = false
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
            add_submit(name) {
                //添加_提交
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            Job_title: this.formLeft.Job_title_input,
                            Job_content: this.formLeft.Job_content_input,
                            Execution_host: this.formLeft.Execution_host_select,
                            Script_content: this.formLeft.Script_content_input,
                            Approver: this.formLeft.Approver_select,
                            Approver_display: this.formLeft.Approver_display,
                        }
                        this.$api.User.add_submit(params).then(res => {
                            if (res.result) {
                                this.success('提交成功！')
                                this.get_work_management()
                                this.calbac()
                                this.add_status = false
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
            modify_work_management(row) {
                // 修改工单按钮
                this.oldData.Job_title_input = row.Job_title
                this.oldData.Job_content_input = row.Job_content
                this.oldData.Execution_host_select = row.Execution_host
                this.oldData.Script_content_input = row.Script_content
                this.oldData.Approver_select = row.Approver
                this.oldData.Approver_display = row.Approver_display
                this.oldData.id = row.id
                this.get_host();
                this.get_allUser();
            },
            modify_save_wm(name) {
                //修改_确定按钮
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            Job_title: this.oldData.Job_title_input,
                            Job_content: this.oldData.Job_content_input,
                            Execution_host: this.oldData.Execution_host_select,
                            Script_content: this.oldData.Script_content_input,
                            Approver: this.oldData.Approver_select,
                            Approver_display: this.oldData.Approver_display,
                            id: this.oldData.id
                        };
                        this.$api.User.modify_save_wm(params).then(res => {
                            if (res.result) {
                                this.success('修改成功！')
                                this.get_work_management()
                                this.modify_status = false
                            }
                        })
                    } else {
                        this.loading_modify = false;
                        setTimeout(() => {
                            this.$nextTick(() => {
                                this.loading_modify = true;
                            });
                        }, 300)
                        this.loading = false
                    }
                })
            },
            submit(row) {
                //提交
                let params = {
                    id: row.id
                }
                this.$api.User.submit(params).then(res => {
                    if (res.result) {
                        this.success('提交成功！')
                        this.get_work_management()
                    }
                })
            },
            delete_work_management(row) {
                // 删除工单按钮
                let params = {
                    id: row.id
                }
                this.$api.User.delete_work_management(params).then(res => {
                    if (res.result) {
                        this.get_work_management()
                        this.error('删除成功！')
                    }
                })
            },
            get_work_management() {
                // 获取未提交的工单信息
                this.$api.User.get_work_management().then(res => {
                    this.data = res.data
                })
            },
            calbac() {
                // 添加工单取消&回调
                this.$refs['formLeft'].resetFields()
                this.$refs['oldData'].resetFields()
                this.add_status = false
                this.modify_status = false
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
            perChange(e) {
                //触发选择审批人
                this.formLeft.Approver_select = e.value
                this.formLeft.Approver_display = e.label
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
        }
    }
</script>

<style scoped>

</style>
