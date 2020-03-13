<template>
    <div id="iViewTwo">
        <Row>
            <Col span="8">
                <h3 class="">表单</h3>
                <div class="padding-top10">
                    <Form ref="forms" :model="formItem" :label-width="80">
                        <FormItem label="输入框"
                                  prop="input"
                                  :rules="{required: true, message: '输入框不能为空', trigger: 'blur'}">
                            <Input v-model="formItem.input" placeholder="请输入"></Input>
                        </FormItem>
                        <FormItem label="单选框">
                            <RadioGroup v-model="formItem.radio">
                                <Radio label="male">男</Radio>
                                <Radio label="female">女</Radio>
                            </RadioGroup>
                        </FormItem>
                        <FormItem label="选择器">
                            <Select v-model="formItem.select" v-validate="'required'"
                                    name="选择器">
                                <Option value="beijing">New York</Option>
                                <Option value="shanghai">London</Option>
                                <Option value="shenzhen">Sydney</Option>
                            </Select>
                        </FormItem>
                        <FormItem label="选择器">
                            <Select v-model="formItem.select">
                                <Input v-model="searchText" search @on-search='searchItem()'
                                       style="width: 200px" class="margin-left10 margin-bottom10"></Input>
                                <Option value="beijing">New York</Option>
                                <Option value="shanghai">London</Option>
                                <Option value="shenzhen">Sydney</Option>
                            </Select>
                        </FormItem>
                        <FormItem label="多选框">
                            <CheckboxGroup v-model="formItem.checkbox">
                                <Checkbox label="吃"></Checkbox>
                                <Checkbox label="睡"></Checkbox>
                                <Checkbox label="跑"></Checkbox>
                                <Checkbox label="玩"></Checkbox>
                            </CheckboxGroup>
                        </FormItem>
                        <FormItem label="开关选择器">
                            <i-switch v-model="formItem.switch" size="large">
                                <span slot="open">On</span>
                                <span slot="close">Off</span>
                            </i-switch>
                            <Button type="primary" class="margin-left20" @click="confirmData()">校验</Button>
                            <Button type="error" class="margin-left20" @click="clearVal()">清除</Button>
                        </FormItem>
                        <FormItem label="滑动条">
                            <Slider v-model="formItem.slider" range></Slider>
                        </FormItem>
                        <FormItem label="文本框">
                            <Input v-model="formItem.textarea" type="textarea" :autosize="{minRows: 2,maxRows: 5}"
                                   placeholder="请输入"></Input>
                        </FormItem>
                    </Form>
                </div>
            </Col>
            <Col span="8" push="3">
                <h3>进度条</h3>
                <div class="margin-top10 padding-left10">
                    <el-steps :active="2" align-center finish-status="success">
                        <el-step title="步骤1" description="111"></el-step>
                        <el-step title="步骤2" description="222"></el-step>
                        <el-step title="步骤3" description="333"></el-step>
                        <el-step title="步骤4" description="444"></el-step>
                    </el-steps>
                </div>
                <el-steps :active="1" finish-status="success" align-center simple class="margin-top20">
                    <el-step title="步骤 1"></el-step>
                    <el-step title="步骤 2" icon="el-icon-refresh-left" class="cw-step-pro cw-step-process"></el-step>
                    <el-step title="步骤 3" class="cw-step-pro"></el-step>
                </el-steps>
                <h3 class="margin-top20">时间轴</h3>
                <div class="margin-top10 padding-left10 float-left">
                    <Timeline pending>
                        <TimelineItem
                            v-for="item in timeList"
                            :key="item.time">
                            <Icon type="md-checkmark-circle"
                                  slot="dot"
                                  v-if="item.type==='done'"/>
                            <Icon type="ios-radio-button-on"
                                  slot="dot" color="#999"
                                  v-if="item.type==='future'"/>
                            <p>{{item.time}}</p>
                            <p>{{item.content}}</p>
                        </TimelineItem>
                    </Timeline>
                </div>
                <div class="margin-top10 margin-left20 padding-left10 float-left">
                    <Timeline pending>
                        <TimelineItem
                            v-for="item in timeList"
                            :key="item.time">
                            <Icon type="ios-radio-button-on"
                                  slot="dot" color="#217FC3" v-if="item.type==='done'"/>
                            <Icon type="ios-radio-button-on"
                                  slot="dot" color="#FEA30D" v-if="item.type==='now'"/>
                            <Icon type="ios-radio-button-on"
                                  slot="dot" color="#ED3F3F" v-if="item.type==='future'"/>
                            <p>{{item.time}}</p>
                            <p>{{item.content}}</p>
                        </TimelineItem>
                    </Timeline>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
    export default {
        name: 'iViewTwo',
        data() {
            return {
                searchText: '',
                formItem: {
                    input: '',
                    select: '',
                    radio: 'male',
                    checkbox: [],
                    switch: true,
                    date: '',
                    time: '',
                    slider: [20, 50],
                    textarea: ''
                },
                timeList: [
                    {
                        time: '1976年',
                        content: 'Apple I 问世',
                        type: 'done'
                    },
                    {
                        time: '2007年',
                        content: '发布 iPhone',
                        type: 'now'
                    },
                    {
                        time: '2010年',
                        content: '发布 iPad',
                        type: 'future'

                    }
                ]
            }
        },
        methods: {
            confirmData() {
                this.$refs['forms'].validate((valid) => {
                    if (valid) {
                        // this.paramAdd(this.data);
                    }
                })
                // this.$validator.validate().then(valid => {
                //     if (valid) {
                // this.paramAdd(this.data);
                // }
                // });
            },
            clearVal() {
                // this.$validator.errors.clear();
                this.$refs['forms'].resetFields();
            }
        }
    }
</script>

<style scoped>

</style>
