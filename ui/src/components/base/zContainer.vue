<template>
    <div id="main-container">
        <div style="width: calc(100%);">
            <Content :style="{padding: '0 110px', margin: '20px 0'}">
                <Card>
                    <div >
                        <router-view  style="min-height: 200px;" class="padding-10"/>
                    </div>
                </Card>
            </Content>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'zContainer',
        props: {
            menuList: {}
        },
        components: {},
        data() {
            return {
                showLeftMenu: false,
                coMenu: {},
                appType: '',
                leftWidth: '65px',
                colState: true
            }
        },
        created() {
            //lal
        },
        methods: {
            menuChange(data) {
                this.coMenu = data;
            },
            colChange(data) {
                this.colState = data
                this.leftWidth = data ? '65px' : '17%'
            }
        },
        watch: {}
    }
</script>

<style lang="scss" scoped>
    $headerHeight: 60px;
    #main-container {
        width: 100%;
        background: #fff;
        top: $headerHeight;
        position: absolute;
        display: flex;
        overflow: hidden;

        .full-width {
            width: 100% !important;
        }

        .col-left {
            width: calc(100% - 65px) !important;
        }

        .top-menu {
            height: 30px;
            font-size: 14px;
            line-height: 30px;
            padding-left: 16px;
            vertical-align: bottom;
            border-bottom: 1px solid #e3e5e8;
        }
    }
</style>

