<template>
    <div id="cw-table" ref="block">
        <div id="cw-table-box" class="cw-table-box" :style="{height:  'calc(100% - '+(cutHeight - 20) + 'px' +')'}">
            <Table
                :ellipsis="ellipsis"
                :tooltip="tooltip"
                :border="true"
                :columns="columnsNew"
                :data="pageData"
                :stripe="stripe"
                :height="tableHeight"
                @on-row-click="rowClick"
                @on-selection-change="selectionChange"
            >
            </Table>
            <div class="cw-table-footer" ref="table">
                <el-pagination v-if="showFooter"
                               :current-page="page.pageNum"
                               :page-sizes="pageSizes"
                               :page-size="nowPageSize"
                               :pager-count="pagerCount"
                               :layout="layout"
                               :total="pageTotal"
                               :height="footerHeight"
                               :popper-class="popperClass"
                               @size-change="sizeChange"
                               @current-change="currentChange"
                               @prev-click="prevClick"
                               @next-click="nextClick">
                </el-pagination>
            </div>
        </div>
        <Drawer class="drawer" :title="rightMenu.title" :closable="closable" v-model="closable" width="800">
            <ul>
                <li style="float: left;width: 50%;line-height: 35px;display: flex"
                    v-for="(val, key, index) of instObj" :key="index">
                    <span
                        style="width: 100px;text-align: right;padding: 0 10px;overflow: hidden;white-space: nowrap;color:#737987;">
                        {{key}}:
                    </span>
                    <span :title="val"
                          style="color:#333948;text-align: left;flex: 1;text-overflow: ellipsis;white-space: nowrap;padding: 0 10px;overflow: hidden">
                        {{val}}
                    </span>
                </li>
            </ul>
        </Drawer>
    </div>
</template>

<script>
    import jquery from 'jquery'

    var storage = window.localStorage;
    export default {
        name: 'cw-table',
        props: {
            popperClass: {
                default: '条/个'
            },
            cwheight: {},
            cutHeight: {
                default: 0
            },
            stripe: {
                default: false
            },
            noDataText: {
                default: '暂无数据'
            },
            tooltip: {
                default: true
            },
            ellipsis: {
                default: true
            },
            remote: {
                default: false
            },
            showFooter: {
                default: true
            },
            columns: {
                default: function () {
                    return [
                        {
                            title: '默认列',
                            key: 'cloud_name',
                            sortable: true,
                            width: 100
                        }
                    ]
                }
            },
            data: {
                default: function () {
                    return []
                },
                type: Array
            },
            page: {
                default: function () {
                    return {
                        pageNum: 1,
                        page_size: 10,
                    }
                }
            },
            total: {
                default: 1
            },
            pagerCount: {
                default: 5
            },
            pageSizes: {
                default: function () {
                    return [10, 20, 50, 100]
                }
            },
            layout: {
                default: 'total, sizes, prev, pager, next, jumper'
            },
            rightMenu: {
                default: function () {
                    return {
                        title: '实例信息',
                        status: false
                    }
                }
            }
        },
        components: {},
        data() {
            return {
                screenHeight: document.body.clientHeight,
                defaultTableHeight: 500,
                columnsNew: [],
                tableHeight: 460,
                footerHeight: 40,
                pageData: [],
                closable: false,
                instObj: {},
                pageTotal: 0,
                nowPageSize: 10,
            }
        },
        mounted() {
            // <CwTable :cutHeight="40" :cwheight=0 :columns="pro_table_titles":data="Reserveplans"></CwTable>    引入格式：  cwheight可以自适应高度 也可以给高度 如果自适应 cwheight给0就ok
            //初始值 页面加载就进行自适应 topdistance是距离顶部距离 -10是为了有些border占用1px
            let topdistance = parseInt($('#cw-table').offset().top)
            if (this.cwheight == 0) {
                this.$refs.block.style.height = window.innerHeight - topdistance - 10 + 'px'
                this.tableHeight = window.innerHeight - topdistance - 60 - ((window.innerHeight - topdistance - 10 - 60) * 0.09)
                this.footerHeight = window.innerHeight - topdistance - 60 - this.tableHeight
            } else {
                this.$refs.block.style.height = this.cwheight
                this.tableHeight = this.cwheight
            }
            if (storage.getItem('pagesize') != null) {
                this.nowPageSize = parseInt(storage.pagesize)
            }
            this.initColumns();
            this.initPage();
            this.$nextTick(() => {
            })
            const that = this
            window.onresize = () => {
                return (() => {
                    let topdistance = parseInt($('#cw-table').offset().top)
                    if (this.cwheight == 0) {
                        this.$refs.block.style.height = window.innerHeight - topdistance - 10 + 'px'
                        this.tableHeight = window.innerHeight - topdistance - 60 - ((window.innerHeight - topdistance - 60 - 10) * 0.09)
                        this.footerHeight = window.innerHeight - topdistance - 60 - this.tableHeight
                    } else {
                        this.$refs.block.style.height = this.cwheight
                        this.tableHeight = this.cwheight
                    }
                })()
            }
        },
        watch: {
            columns: function () {
                this.initColumns();
            },
            data: function () {
                this.initPage();
            },
            page: function () {
                this.initPage();
            },
            total: function (total) {
                this.total = total;
                this.initPage();
            },
            screenHeight(val) {
                // 为了避免频繁触发resize函数导致页面卡顿，使用定时器
                if (!this.timer) {
                    // 一旦监听到的screenWidth值改变，就将其重新赋给data里的screenWidth
                    this.timer = true
                    let that = this
                    setTimeout(function () {
                        // 打印screenWidth变化的值
                        that.timer = false
                    }, 400)
                }
            }
        },
        methods: {
            initColumns() {
                let columnsNew = [];
                this.columns.forEach((item, index) => {
                    if (this.ellipsis) {
                        item['ellipsis'] = true
                    }
                    // if (this.tooltip) {
                    //     item['tooltip'] = true
                    // }
                    columnsNew.push(item);
                });
                if (columnsNew.length !== 0) {
                    this.columnsNew = columnsNew;
                } else {
                    this.columnsNew = [
                        {
                            title: '列一',
                            key: 'cloud_name',
                            sortable: true
                        }
                    ];
                }
            },
            initPage() {
                if (!this.remote) {
                    this.pageData = [];
                    this.pageTotal = this.data.length;
                    this.data.forEach((item, index) => {
                        let start = this.nowPageSize * (this.page.pageNum - 1);
                        let end = this.nowPageSize * this.page.pageNum;
                        if (start < (index + 1) && (index + 1) <= end) {
                            this.pageData.push(item);
                        }
                    });
                } else {
                    this.pageTotal = this.total;
                    this.pageData = this.data;
                }
            },
            sizeChange(size) {
                storage.pagesize = size
                this.nowPageSize = parseInt(storage.pagesize)
                if (this.remote) {
                    this.$emit('sizeChange', size);
                    this.$emit('pageChange', this.page);
                } else {
                    this.initPage();
                }
            },
            currentChange(pageNum) {
                this.page.pageNum = pageNum;
                if (this.remote) {
                    this.$emit('currentChange', pageNum);
                    this.$emit('pageChange', this.page);
                } else {
                    this.initPage();
                }
            },
            nextClick(pageNum) {
                this.page.pageNum = pageNum;
                if (this.remote) {
                    this.$emit('nextClick', pageNum);
                    this.$emit('pageChange', this.page);
                } else {
                    this.initPage();
                }
            },
            prevClick(pageNum) {
                this.page.pageNum = 2;
                if (this.remote) {
                    this.$emit('prevClick', pageNum);
                    this.$emit('pageChange', this.page);
                } else {
                    this.initPage();
                }
            },
            rowClick(row) {
                if (this.rightMenu.status) {
                    this.showDrawer(row, this.rightMenu.columns);
                } else {
                    this.$emit('rowClick', row)
                }
            },
            selectionChange(targetRows) {
                this.$emit('on-selection-change', targetRows);
            },
            showDrawer(row, columns) {
                this.closable = true;
                let colObj = {};
                if (columns) {
                    columns.forEach((item, index) => {
                        colObj[item.key] = item.title;
                    });
                } else {
                    this.columnsNew.forEach((item, index) => {
                        colObj[item.key] = item.title;
                    });
                }
                Object.keys(row).forEach((key) => {
                    if (colObj.hasOwnProperty(key)) {
                        let title = colObj[key];
                        this.instObj[title] = row[key];
                    }
                })
            }
        }
    }
</script>

<style scoped lang="scss">
    #cw-table {
        width: 100%;
        height: 100%;
        .cw-table-box {
            margin-top: 20px;
            position: relative;
            border-right: none;
            .cw-table-footer {
                border: 1px solid #dde4eb;
                background: #fafbfd;
                width: 100%;
                position: absolute;
                /*bottom: 5px;*/
                z-index: 9;
                text-align: right;
                padding-right: 10px;
                line-height: 40px;
                padding-top: 4px;
            }
        }
    }
</style>
<!--iview表格样式-->
<style lang="scss" scoped>
    html, body {
        height: 100%
    }

    #cw-table {
        .ivu-table {
            overflow-x: hidden;
            color: #4d5669 !important;
            .ivu-table-overflowY::-webkit-scrollbar { /*滚动条整体样式*/
                width: 7px; /*高宽分别对应横竖滚动条的尺寸*/
                height: 4px;
            }
            .ivu-table-overflowY::-webkit-scrollbar-thumb { /*滚动条里面小方块*/
                border-radius: 5px;
                -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
                background: #a5a5a5;
            }
        }
        .ivu-table-body {
            overflow-x: hidden;
        }
        .ivu-table td {
            height: 40px !important;
            border-bottom: 1px solid #dde4eb;
        }

        .ivu-table th {
            background: #fafbfd;
            font-size: 14px !important;
            font-weight: 200 !important;
            height: 40px !important;
            border-bottom: 1px solid #dde4eb !important;
            border-right: 1px solid #dde4eb !important;
        }

        .ivu-table-header th:nth-last-child(2) {
            border-right: none;
        }

        .ivu-table-body table {
            width: 100% !important;
        }

        .ivu-table:before {
            background: #fff;
        }
        .ivu-table:after {
            width: 0;
        }
        .ivu-table-border td {
            border-right: none;
        }

        .ivu-table th .ivu-table-cell {
            white-space: nowrap;
        }

        .ivu-table-stripe .ivu-table-body tr:nth-child(2n) td, .ivu-table-stripe .ivu-table-fixed-body tr:nth-child(2n) td {
            background: #fafbfd !important;
        }
        .ivu-table-wrapper {
            border-right: 1px solid #dde4eb;
        }

    }

    // 抽屉
    .ivu-drawer-header {
        height: 60px !important;
        line-height: 60px !important;
        padding: 0 16px !important;
        background: #f9f9f9;
    }

    .ivu-drawer-header-inner {
        height: 60px;
        line-height: 60px !important;
    }
</style>
<!--element分页样式-->
<style>
    #cw-table .el-pagination {
        color: #4d5669;
        font-weight: 200;
    }

    #cw-table .btn-prev {
        border: 1px solid #ddd !important;
        border-right: none !important;
    }

    #cw-table .btn-next {
        border: 1px solid #ddd !important;
    }

    #cw-table .el-pager li:hover {
        border: 1px solid rgb(60, 150, 255) !important;
        border-right: none;
    }

    #cw-table .el-pager li {
        border: 1px solid #ddd;
        border-right: none;
    }

    #cw-table .el-pager .active {
        background: rgb(60, 150, 255);
        border: 1px solid rgb(60, 150, 255) !important;
        color: #fff !important;
    }

    #cw-table .el-select-dropdown {
        box-shadow: none;
        max-width: 100px;
        min-width: 100px !important;
    }

    #cw-table .ivu-table-tip {
    }

    #cw-table .ivu-table {
    }
</style>
