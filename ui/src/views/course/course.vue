<template>
    <div id="course">
        <Header>
            <Row type="flex" align="middle" class="code-row-bg">
                <Col span="12" align="middle" class="grid-content bg-purple">
                    <Input @on-blur="getDataPage" v-model="seText" search enter-button @on-search="searchUser()"
                           placeholder="请输入用户名搜索"/>
                </Col>
                <Col span="12" push="10" class="grid-content bg-purple">
                    <el-button type="primary" size="mini"
                               @click="modal1 = true,modal_load=true">添加
                    </el-button>
                </Col>
            </Row>

        </Header>
        <Content>
            <template>
                <Table height="300" border :columns="columns12" :data="data6">
                    <template slot-scope="{ row, index }" slot="username">
                        <Input type="text" v-model="usernameEdit" v-if="editIndex === index"/>
                        <span v-else>
                        <strong>{{ row.username }}</strong>
                    </span>
                    </template>
                    <template slot-scope="{ row, index }" slot="phone">
                        <Input type="text" v-model="phoneEdit" v-if="editIndex === index"/>
                        <span v-else>{{ row.phone }}</span>
                    </template>
                    <template slot-scope="{ row, index }" slot="goods">
                        <Input type="text" v-model="goodsEdit" v-if="editIndex === index"/>
                        <span v-else>{{ row.goods }}</span>
                    </template>
                    <template slot-scope="{ row, index }" slot="price">
                        <Input type="text" v-model="priceEdit" v-if="editIndex === index"/>
                        <span v-else>{{ row.price }}</span>
                    </template>
                    <template slot-scope="{ row, index }" slot="ordNum">
                        <Input type="text" v-model="ordNumEdit" v-if="editIndex === index"/>
                        <span v-else>{{ row.ordNum }}</span>
                    </template>
                    <template slot-scope="{ row, index }" slot="action">
                        <div v-if="editIndex === index">
                            <Button type="success" size="small" @click="handleSave(row,index)">保存</Button>
                            <Button type="error" size="small" @click="editIndex = -1">取消</Button>
                        </div>
                        <div v-else>
                            <Button type="primary" size="small" style="margin-right: 5px"
                                    @click="handleEdit(row, index)">
                                修改
                            </Button>
                            <Button type="error" size="small" @click="remove(row)">删除</Button>
                        </div>
                    </template>
                </Table>
            </template>
            <template>
                <Row type="flex" align="middle" class="code-row-bg">
                    <Col span="12" push="6">
                        <Page
                            :current=onPage
                            :total=Total
                            :page-size=PageSize
                            @on-change="change_page"
                            @on-page-size-change="change_pageSize"
                            :page-size-opts="[5, 10, 15, 20]"
                            show-total show-sizer show-elevator/>
                    </Col>
                </Row>
            </template>
        </Content>
        <template>
            <!--弹窗-->
            <Modal
                v-model=modal1
                :loading=modal_load
                title="添加用户信息"
                @on-ok="add('formInline')"
                @on-cancel="calbac()">
                <Form ref="formInline" :model="formInline" :rules="ruleInline" inline>
                    <FormItem label="用户名：" prop="usernameNew">
                        <Input type="text" v-model="formInline.usernameNew" placeholder="用户名"></Input>
                        <Icon type="ios-person-outline" slot="prepend"></Icon>
                    </FormItem>
                    <FormItem label="电话：" prop="phoneNew">
                        <Input type="number" v-model="formInline.phoneNew" placeholder="电话"></Input>
                    </FormItem>
                    <FormItem label="商品：" prop="goodsNew">
                        <Input type="text" v-model="formInline.goodsNew" placeholder="商品"></Input>
                    </FormItem>
                    <FormItem label="价格：" prop="priceNew">
                        <Input type="number" v-model="formInline.priceNew" placeholder="价格"></Input>
                    </FormItem>
                    <FormItem label="订单号：" prop="ordNumNew">
                        <Input type="number" v-model="formInline.ordNumNew" placeholder="订单号"></Input>
                    </FormItem>
                </Form>
            </Modal>
        </template>
    </div>
</template>

<script>
    export default {
        name: 'course',
        props: {},
        data() {
            return {
                columns12: [
                    {
                        title: '用户名',
                        slot: 'username'
                    },
                    {
                        title: '电话',
                        slot: 'phone'
                    },
                    {
                        title: '商品',
                        slot: 'goods'
                    },
                    {
                        title: '价格',
                        slot: 'price'
                    },
                    {
                        title: '订单号',
                        slot: 'ordNum'
                    },
                    {
                        title: 'Action',
                        slot: 'action',
                        width: 150,
                        align: 'center'
                    }
                ],
                data6: [],
                dataLast: [],
                //分页属性
                Total: '',
                PageSize: 5,
                OnPage: 1,
                //搜索信息
                seText: '',
                //修改信息
                usernameEdit: '',
                phoneEdit: '',
                goodsEdit: '',
                priceEdit: '',
                ordNumEdit: '',
                editIndex: -1,
                formInline: {
                    //新增信息
                    usernameNew: '',
                    phoneNew: '',
                    goodsNew: '',
                    priceNew: '',
                    ordNumNew: '',
                },
                ruleInline: {
                    //表单检验
                    usernameNew: [
                        {required: true, message: '请输入用户名', trigger: 'blur'}
                    ],
                    phoneNew: [
                        {required: true, message: '请输入电话', trigger: 'blur'}
                    ],
                    goodsNew: [
                        {required: true, message: '请输入商品名', trigger: 'blur'}
                    ],
                    priceNew: [
                        {required: true, message: '请输入价格', trigger: 'blur'}
                    ],
                    ordNumNew: [
                        {required: true, message: '请输入定单号', trigger: 'blur'}
                    ],
                },
                modal1: false,
                modal_load: false,
            }
        },
        computed: {},
        watch: {
            // this.myFunc()
        },
        created() {
            // this.myFunc()
            this.getDataPage()
        },
        mounted() {
            // this.myFunc()
        },
        methods: {
            //改变页码
            change_page(val) {
                this.OnPage = val
                this.getDataPage()
            },
            //改变每页显示条数
            change_pageSize(val) {
                this.PageSize = val
                this.getDataPage()
            },
            //获取分页后页面
            getDataPage() {
                let params = {
                    pageSize: this.PageSize,
                    on_page: this.OnPage,
                }
                this.$api.User.getShopInfo(params).then(res => {
                    if (res.result) {
                        this.data6 = res.data
                        this.Total = res.sizeAll
                    } else {
                        alert('错误')
                    }
                })
            },
            // 添加_确定
            add(name) {
                this.$refs[name].validate((valid) => {
                    if (valid) {
                        let params = {
                            username: this.formInline.usernameNew,
                            phone: this.formInline.phoneNew,
                            goods: this.formInline.goodsNew,
                            price: this.formInline.priceNew,
                            ordNum: this.formInline.ordNumNew,
                        }
                        this.$api.User.addInfo(params).then(res => {
                            if (res.result) {
                                this.$message('添加成功！');
                                this.modal1 = false
                                this.getDataPage()
                            }
                        })
                        this.calbac()
                    } else {
                        this.modal1 = true
                        this.$message('添加失败！');
                        setTimeout(() => {
                            this.modal1 = false;
                        }, 2000);
                        return false;
                    }
                })
            },
            //修改
            handleEdit(row, index) {
                this.usernameEdit = row.username;
                this.phoneEdit = row.phone;
                this.goodsEdit = row.goods;
                this.priceEdit = row.price;
                this.ordNumEdit = row.ordNum;
                this.editIndex = index;
            },
            //保存修改
            handleSave(row, index) {
                let params = {
                    username: this.usernameEdit,
                    phone: this.phoneEdit,
                    goods: this.goodsEdit,
                    price: this.priceEdit,
                    ordNum: this.ordNumEdit,
                    id: row.id,
                }
                this.$api.User.editInfo(params).then(res => {
                    if (res.result) {
                        this.getDataPage()
                    }
                })
                this.editIndex = -1;
            },
            //删除
            remove(row) {
                let params = {
                    id: row.id
                }
                this.$api.User.removeInfo(params).then(res => {
                    if (res.result) {
                        this.getDataPage()
                    }
                })
            },
            //取消回调
            calbac() {
                this.formInline = {
                    usernameNew: '',
                    phoneNew: '',
                    goodsNew: '',
                    priceNew: '',
                    ordNumNew: '',
                }
            },
            //搜索
            searchUser() {
                let params = {
                    seText: this.seText
                }
                this.dataLast = this.data6
                this.$api.User.searchText(params).then(res => {
                    if (res.result) {
                        if (res.data) {
                            this.data6 = [res.data]
                        } else {
                            this.getDataPage()
                        }
                    }
                })
            },
        }
    }
</script>

<style scoped lang="scss">
    #course {
        color: $base-color;
    }
</style>
