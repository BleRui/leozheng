<template>
    <div id='app' @click="cancel">
        <z-Header :menu-list="menuList"></z-Header>
        <z-Container :style="{height: 'calc(100% - '+ 60 + 'px' +')' }"></z-Container>
    </div>
</template>

<script>
    import zHeader from '@/components/base/zHeader'
    import zContainer from '@/components/base/zContainer'

    export default {
        name: 'WorkManage',
        components: {
            zHeader,
            zContainer,
        },
        data() {
            return {
                menuList: [
                    {
                        name: 'Work_manage',
                        cnName: '工单管理',
                        to: '/Work_manage',
                        icon: 'el-icon-location',
                        hasChild: false,
                    },
                    {
                        name: 'Approval_manage',
                        cnName: '审批管理',
                        to: '/Approval_manage',
                        icon: 'el-icon-location',
                        hasChild: false,
                    },
                    {
                        name: 'Job_history',
                        cnName: '工单历史',
                        to: '/Job_history',
                        icon: 'el-icon-location',
                        hasChild: false,
                    }]
            }
        },
        methods: {
            cancel() {
            },
            getHeight() {
                let headerHeight = 60;
                if (window.innerHeight) {
                    this.winHeight = window.screen.availHeight - (window.outerHeight - window.innerHeight);
                }
                // if (document.documentElement && document.documentElement.clientHeight && document.documentElement.clientWidth) {
                //     this.winHeight = document.documentElement.clientHeight;
                // }
                this.winHeight = this.winHeight - headerHeight + 'px'
            }
        }
    }
</script>

<style lang="scss">
    html, body {
        height: 100%;
    }

    ::-webkit-scrollbar-thumb:window-inactive {
        background: rgba(255, 0, 0, .4)
    }
</style>
