<template>
    <div id="dropDown">
        <Dropdown transfer :trigger="actionType" :visible="showMenu" @on-click="showMe">
            <Button :type="type" @click="showMenu=!showMenu">
                下拉菜单
                <Icon type="ios-arrow-down"></Icon>
            </Button>
            <DropdownMenu slot="list" :class="{'primary-drop-down':type==='primary'}" disabled>
                <DropdownItem disabled class="drop-down-input" v-if="search" name="cw-search">
                    <Input v-model="dropSearch" search style="width: 80px"></Input>
                </DropdownItem>
                <DropdownItem class="margin-top5"
                              v-for="item in dropList"
                              :key="item.name"
                              :name="item.disable?'cw-search':item.name"
                              :disabled="item.disable">
                    {{item.name}}
                </DropdownItem>
            </DropdownMenu>
        </Dropdown>
    </div>
</template>

<script>
    export default {
        /**
         * 参考: https://www.iviewui.com/components/dropdown
         * @param {boolean} search 是否显示搜索框
         * @param {string} type 按钮样式
         * @param {string} actionType 触发下拉方式 hover（悬停）click（点击）contextMenu（右键）custom（自定义）
         * @param {list} dropBack 下拉展示数据
         */
        name: 'CWDropDown',
        props: {
            actionType: {
                type: String,
                default() {
                    return 'hover'
                }
            },
            type: {
                type: String,
                default() {
                    return 'default'
                }
            },
            search: {
                type: Boolean,
                default() {
                    return false
                }
            },
            dropBack: {
                default() {
                    return [
                        {
                            name: '驴打滚',
                            disable: false,
                        },
                        {
                            name: '炸酱面',
                            disable: false,
                        },
                        {
                            name: '冰糖葫芦',
                            disable: true,
                        },
                        {
                            name: '北京烤鸭',
                            disable: false,
                        },
                    ]
                }
            },
        },
        data() {
            return {
                dropSearch: '',
                showMenu: false
            }
        },
        computed: {
            dropList() {
                return this.dropBack.filter((item) => {
                    return item.name.indexOf(this.dropSearch) !== -1
                })
            }
        },
        methods: {
            showMe(data) {
                if (data !== 'cw-search') {
                    this.showMenu = false;
                    this.$emit('menuDrop', data);
                }
            }
        }
    }
</script>

<style scoped>
    #dropDown {
    }
</style>
