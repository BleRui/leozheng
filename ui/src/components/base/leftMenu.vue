<template>
    <div id="left-menu">
        <Menu :active-name="defaultActive" accordion :open-names="seFather" @on-select="selectChild"
              @on-open-change="selectItem" ref="leftMenu">
            <div v-for="item in menuList" :key="item.name">
                <MenuItem class="font-16"
                          :name="item.name"
                          :to="item.to" v-if="!item.hasChild" :class="{'homeSe':item.name===defaultActive}">
                    <Icon :type="item.icon"/>
                    {{item.cnName}}
                </MenuItem>
                <Submenu :name="item.name"
                         v-if="item.hasChild" :class="{'second-selected':item.name===seFather[0]}">
                    <template slot="title">
                        <Icon :type="item.icon"/>
                        {{item.cnName}}
                    </template>
                    <div v-for="child in item.children" :key="child.name">
                        <MenuItem v-if="!child.hasChild" :class="{'seOpen':child.name===defaultActive}"
                                  :name="child.name"
                                  :to="child.to">
                            {{child.cnName}}
                        </MenuItem>
                        <Submenu v-if="child.hasChild"
                                 :name="child.name"
                                 class="second-menu"
                                 :class="{'second-selected':child.name===seFather[1]}">
                            <template slot="title">
                                {{child.cnName}}
                            </template>
                            <MenuItem v-for="third in child.children"
                                      :class="{'seOpen':third.name===defaultActive}"
                                      :key="third.name"
                                      :name="third.name"
                                      :to="third.to">
                                {{third.cnName}}
                            </MenuItem>
                        </Submenu>
                    </div>
                </Submenu>
            </div>
        </Menu>
    </div>
</template>

<script>
    export default {
        name: 'leftMenu',
        props: {
            menuList: {}
        },
        data() {
            return {
                defaultActive: '',
                openName: [],
                seFather: [],
                isCollapse: true
            }
        },
        created() {
            this.defaultActive = this.$route.name;
            this.getParent();
            let data = this.$route.meta.title;
            this.$emit('menuChange', data)
        },
        watch: {
            $route: function () {
                let data = this.$route.meta.title;
                this.$emit('menuChange', data)
            }
        },
        methods: {
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
            selectChild(name) {
                let data = this.menuList;
                this.defaultActive = name;
                this.seFather = this.openName;
                for (let i = 0; i < data.length; i++) {
                    if (data[i].name === name && !data[i].hasChild) {
                        this.seFather = [];
                        this.$nextTick(() => {
                            this.$refs.leftMenu.updateOpened();
                        });
                    } else if (data[i].name === this.seFather[0]) {
                        for (let j = 0; j < data[i].children.length; j++) {
                            if (data[i].children[j].name === name && !data[i].children[j].hasChild) {
                                if (this.openName.length === 2) this.seFather = this.openName.splice(0, 1);
                                this.$nextTick(() => {
                                    this.$refs.leftMenu.updateOpened();
                                });
                            }
                        }
                    }
                }
            },
            selectItem(name) {
                this.openName = name;
            }
        }
    }
</script>
<style lang="scss" scoped>
    $headerHeight: 60px;
    #left-menu {
        width: 17%;
        height: 100%;
        background-color: #fff;
        border-right: 1px solid #e3e5e8;

        .ivu-menu {
            width: 100% !important;

        }

        .el-menu {
            border: none;
        }

        .ivu-icon {
            font-size: 20px;
            padding-right: 10px;
        }

        .ivu-menu-vertical.ivu-menu-light:after {
            content: '';
            width: 0 !important;
            display: none !important;
        }
    }

</style>
