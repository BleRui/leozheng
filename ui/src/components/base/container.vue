<template>
    <div id="main-container">
        <LeftMenu v-if="showLeftMenu"
                  :style="{width: leftWidth}"
                  @menuChange="menuChange"
                  @colChange="colChange"
                  :menu-list="menuList"></LeftMenu>
        <div :class="{'full-width':!showLeftMenu,'col-left':colState}" style="width: calc(100% - 17%);">
            <div class="top-menu" v-if="showLeftMenu">
                <Icon type="md-home" size="18" style="vertical-align: text-bottom"/>
                <span>{{coMenu}}</span>
            </div>
            <router-view style="height: calc(100% - 30px)" class="padding-10"/>
        </div>
    </div>
</template>

<script>
    // import LeftMenu from '@/components/base/leftMenu'
    import LeftMenu from '@/components/base/eleLeft.vue'

    export default {
        name: 'main-container',
        props: {
            menuList: {}
        },
        components: {
            LeftMenu
        },
        data() {
            return {
                showLeftMenu: true,
                coMenu: {},
                appType: '',
                leftWidth: '65px',
                colState: true
            }
        },
        created() {
            this.showLeftMenu = window.location.href.indexOf('userIndex.html') === -1;
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
