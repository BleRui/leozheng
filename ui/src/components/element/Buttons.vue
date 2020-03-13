<template>
    <div id="Buttons">
        <div class="button-box">
            <h3 class="margin-bottom10">按钮</h3>
            <div class="padding-10">
                <Button>默认</Button>
                <Button type="primary" size="large">主按钮</Button>
                <Button type="dashed" size="small">点点点</Button>
                <Button type="text">文本</Button>
                <br><br>
                <Button type="info">通知</Button>
                <Button type="success">成功</Button>
                <Button type="warning">警告</Button>
                <Button type="error">错误</Button>
            </div>
            <h3 class="margin-bottom10 margin-top20">ghost按钮</h3>
            <div class="ghost-back padding-10">
                <Button ghost>默认</Button>
                <Button type="primary" size="large" ghost>主按钮</Button>
                <Button type="dashed" size="small" ghost>点点点</Button>
                <Button type="text" ghost>文本</Button>
                <br><br>
                <Button type="info" ghost>通知</Button>
                <Button type="success" ghost>成功</Button>
                <Button type="warning" ghost>警告</Button>
                <Button type="error" ghost>错误</Button>
            </div>
            <h3 class="margin-bottom10 margin-top10">按钮disabled</h3>
            <div class="padding-10">
                <Button type="info" disabled>通知</Button>
                <Button type="success" disabled>成功</Button>
                <Button type="warning" disabled ghost>警告</Button>
                <Button type="error" disabled ghost>错误</Button>
            </div>
        </div>
        <div>
            <h3 class="margin-bottom10 margin-top20">图标按钮</h3>
            <div class="padding-10">
                <Button type="primary" icon="ios-search"></Button>
                <Button type="primary" shape="circle" icon="ios-search"></Button>
                <Button type="primary" disabled icon="ios-search"></Button>
            </div>
            <h3 class="margin-bottom10">弹窗</h3>
            <div class="padding-10">
                <Button type="primary" @click="openModal('info')">info</Button>
                <Button @click="openModal('success')">Success</Button>
                <Button @click="openModal('warning')">Warning</Button>
                <Button @click="openModal('error')">Error</Button>
            </div>
            <div class="padding-10">
                <Button @click="openModal('success',2)">Success2</Button>
                <Button @click="openModal('error',2)">Error2</Button>
            </div>
            <div class="padding-10">
                <Button @click="openModal('success',3)">Success3</Button>
                <Button @click="openModal('error',3)">Error3</Button>
            </div>
            <h3 class="margin-bottom10">confirm</h3>
            <div class="padding-10">
                <Button @click="openConfirm('edit')">编辑</Button>
                <Button @click="openConfirm('del')">删除</Button>
            </div>
        </div>
        <div>
            <h3 class="margin-bottom10">下拉菜单</h3>
            <div class="padding-10">
                <div class="dis-inline">
                    <CWDropDown type="primary"></CWDropDown>
                </div>
                <div class="dis-inline">
                    <CWDropDown :search="true" class="margin-top10"></CWDropDown>
                </div>
            </div>
            <h3 class="margin-bottom10 margin-top20">按钮组</h3>
            <div class="padding-10">
                <ButtonGroup class="CW-group-buttons">
                    <Button type="info">按钮1</Button>
                    <Button type="info">按钮2</Button>
                    <Button type="info">按钮3</Button>
                </ButtonGroup>
            </div>
            <div class="padding-10">
                <ButtonGroup class="CW-group-ghost">
                    <Button type="info" ghost>按钮1</Button>
                    <Button type="info" ghost>按钮2</Button>
                    <Button type="info" ghost>按钮3</Button>
                </ButtonGroup>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Buttons',
        methods: {
            openModal(type, style) {
                this.$CWMessage({
                    title: '欢迎',
                    content: '欢迎使用普通对话弹窗',
                    type: type,
                    okText: '确定',
                    style: style
                });
            },
            openConfirm(type) {
                this.$CWConfirm({
                    type: type,
                    title: '删除',
                    content: '是否删除这条数据',
                    okText: '确定',
                    cancelText: '取消',
                }).then(() => {
                    console.log('确定')
                }).catch(() => {
                    console.log('取消')
                });
            }
        }
    }
</script>

<style scoped lang="scss">
    #Buttons {
        display: flex;
        justify-content: space-between;
        .ghost-back {
            background: $split-color;
        }
    }
</style>
