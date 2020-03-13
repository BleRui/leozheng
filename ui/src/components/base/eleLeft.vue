<template>
    <div id="eleLeft">
        <div class="collapse-icon">
            <i class="el-icon-s-unfold" v-if="isCollapse" @click="changeCol()"></i>
            <i class="el-icon-s-fold" v-if="!isCollapse" @click="changeCol()"></i>
        </div>
        <el-menu :default-active="defaultActive"
                 class="el-menu-vertical-demo"
                 @select="selectChild"
                 router
                 unique-opened
                 :collapse-transition="false"
                 :collapse="isCollapse">
            <span v-for="item in menuList" :key="item.name">
                <el-menu-item :index="item.to"
                              v-if="!item.hasChild"
                              :class="{'homeSe':item.to===defaultActive}">
                    <i :class="item.icon"></i>
                    <span slot="title">{{item.cnName}}</span>
                </el-menu-item>
                <el-submenu :index="item.to"
                            :class="{'first-menu':isCollapse,'second-selected':item.name===seFather[0]}"
                            v-if="item.hasChild">
                    <template slot="title">
                        <i :class="item.icon"></i>
                        <span slot="title" v-if="!isCollapse">{{item.cnName}}</span>
                    </template>
                    <div v-for="child in item.children" :key="child.name" class="left-second">
                        <el-menu-item v-if="!child.hasChild"
                                      :index="child.to"
                                      :class="{'homeSe':child.to===defaultActive}">
                            {{child.cnName}}
                        </el-menu-item>
                        <el-submenu :index="child.to"
                                    :class="{'second-selected':child.name===seFather[1]}"
                                    v-if="child.hasChild">
                            <template slot="title">
                                <span slot="title">{{child.cnName}}</span>
                            </template>
                            <el-menu-item v-for="third in child.children"
                                          :key="third.name"
                                          :class="{'homeSe':third.to===defaultActive}"
                                          :index="third.to">
                                {{third.cnName}}
                            </el-menu-item>
                        </el-submenu>
                    </div>
                </el-submenu>
            </span>
        </el-menu>
    </div>
</template>

<script>
    export default {
        name: 'eleLeft',
        props: {
            menuList: {}
        },
        data() {
            return {
                isCollapse: true,
                defaultActive: '',
                seFather: []
            };
        },
        created() {
            this.defaultActive = this.$route.name;
            this.getParent();
            let data = this.$route.meta.title;
            this.$emit('menuChange', data)
            this.$emit('colChange', this.isCollapse)
        },
        watch: {
            $route: function () {
                let data = this.$route.meta.title;
                this.$emit('menuChange', data)
            }
        },
        methods: {
            changeCol() {
                this.isCollapse = !this.isCollapse
                this.$emit('colChange', this.isCollapse)
            },
            getParent() {
                let data = this.menuList;
                for (let i = 0; i < data.length; i++) {
                    if (data[i].hasChild) {
                        for (let j = 0; j < data[i].children.length; j++) {
                            if (data[i].children[j].hasChild) {
                                for (let m = 0; m < data[i].children[j].children.length; m++) {
                                    if (data[i].children[j].children[m].name === this.defaultActive) {
                                        this.seFather.push(data[i].name);
                                        this.seFather.push(data[i].children[j].name);
                                        return;
                                    }
                                }
                            } else if (data[i].children[j].name === this.defaultActive) {
                                this.seFather.push(data[i].name);
                                return;
                            }
                        }
                    }
                }
            },
            selectChild(name, list) {
                this.defaultActive = name;
                this.seFather = list;
            }
        }
    }
</script>

<style scoped>
</style>

<style>
    .collapse-icon {
        position: absolute;
        bottom: 20px;
        left: 20px;
        font-size: 32px;
        cursor: pointer;
    }

    /*.el-menu-vertical-demo:not(.el-menu--collapse) {*/
    /*width: 200px;*/
    /*min-height: 400px;*/
    /*}*/

    .first-menu > .el-submenu__title > .el-submenu__icon-arrow {
        display: none !important;
    }
</style>
