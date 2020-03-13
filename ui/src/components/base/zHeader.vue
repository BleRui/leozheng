<template>
    <div id="cw-header">
        <div class="logo">
            <router-link to="/">
                <img :src="src" style="width: 200px" alt="嘉为蓝鲸">
            </router-link>
        </div>
        <div class="title">
            <router-link to="/Work_manage">
                工单管理
            </router-link>
        </div>
        <div class="menu">
            <HeaderMenu :menu-option="menuOption" :menu-list="menuList" v-if="showMenu"></HeaderMenu>
        </div>
        <div class="user">
            <ul>
                <li>
                    <img class="photo" src="../../assets/base/img/photo.jpg">
                </li>
                <li><span class="username">{{userData.username}}</span></li>
                <li><a :href="logout_url" title="注销登录" class="login-out icon-logout"></a></li>
            </ul>
        </div>
    </div>
</template>

<script>
    import HeaderMenu from '@/components/base/headerMenu'
    import userPath from '../../assets/base/img/logo.png'
    import whiteLogo from '../../assets/base/img/white_logo.png'

    export default {
        name: 'zHeader',
        data() {
            return {
                userData: {},
                username: '123',
                logout_url: '',
                src: whiteLogo,
                showMenu: true,
            }
        },
        props: {
            menuOption: {},
            menuList: {}
        },
        components: {
            HeaderMenu
        },
        created() {
            this.loginUser();
            if (this.headTheme === 'light') {
                this.src = userPath
            } else {
                this.src = whiteLogo
            }
        },
        methods: {
            loginUser() {
                this.$api.Server.homeInfo().then(res => {
                    if (res.result) {
                        this.userData = res.data;
                        this.logout_url = res.data.logout_url;
                    }
                });
            },
        },
    }

</script>

<style lang="scss" scoped>
    $headBackgroundColor: if($head-theme=='light', #fff, $base-color);
    $font-color: if($head-theme=='light', $base-color, #fff);
    #cw-header {
        width: 100%;
        height: $headerHeight;
        border-bottom: 1px solid #ddd;
        position: absolute;
        z-index: 999;
        color: $font-color;
        background: $headBackgroundColor;
        display: flex;
        align-items: center;
    }

    .logo {
        width: 220px;
        align-items: center;
        text-align: center;
    }

    .title {
        width: 200px;
        color: $font-color !important;
        font-size: 24px;
        border-left: 2px solid #c6d7e3;
        padding: 1px 10px 0;

        a {
            color: $font-color !important;
        }
    }

    .menu {
        flex: 1;
    }

    .user {
        height: 100%;
        float: right;
        padding: 1px 8px;

        ul {
            height: 100%;

            li {
                height: 100%;
                float: left;
                line-height: 58px;
                margin: 0 5px;
            }

            li:last-child {
                width: 35px;
                padding-left: 8px;
                cursor: pointer;
            }

            li:last-child:hover {
                color: $white-color !important;
                background-color: $base-hover;

                .icon-logout:before {
                    color: if($head-theme=='light', #ddd, #fff);
                }
            }

            .photo {
                width: 46px;
                height: 46px;
                border-radius: 50px;
                vertical-align: middle;
                display: inline-block;
                border: 1px solid #ddd;
            }

            .customer {
                height: 60%;
                margin-top: 20%;
                border-radius: 10px;
                color: $font-color;
                padding: 0 5px;
                text-align: center;
                line-height: 40px;
                background-color: #37b9ed;
            }

            .username {
                font-size: 18px;
                max-width: 120px;
                white-space: nowrap;
                text-overflow: ellipsis;
                display: inline-block;
                overflow: hidden;
            }

            .login-out {
                font-size: 20px;
                cursor: pointer;
                vertical-align: sub;
                display: inline-block;
            }

            .icon-logout:before {
                color: if($head-theme=='light', #ccc, #fff);
            }

            .icon-logout:hover {
                color: $white-color !important;
            }

        }
    }
</style>
