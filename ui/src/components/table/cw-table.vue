<template>
    <div id="cw-table" style="height: 100%">
        <div id="cw-table-box" class="cw-table-box" :style="{height: 'calc(100% - '+ cutHeight + 'px' +')' }">
            <Table
                :ellipsis="ellipsis"
                :tooltip="tooltip"
                :height="defaultTableHeight"
                :border="true"
                :columns="columnsNew"
                :data="pageData"
                :stripe="stripe"
                @on-select-all-cancel="selectCancel"
                @on-select-all="selectAll"
                @on-select="select"></Table>
            <div class="cw-table-footer">
                <el-pagination v-if="showFooter"
                               :current-page="page.page_num"
                               :page-sizes="pageSizes"
                               :page-size="page.page_size"
                               :pager-count="pagerCount"
                               :layout="layout"
                               :total="page.total_num"
                               :popper-class="popperClass"
                               @size-change="sizeChange"
                               @current-change="currentChange"
                               @prev-click="prevClick"
                               @next-click="nextClick">
                </el-pagination>
            </div>
        </div>
    </div>
</template>

<script>
    import jquery from 'jquery'

    export default {
        name: 'cw-table',
        props: {
            popperClass: {
                default: '条/个'
            },
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
                            title: '列一',
                            key: 'cloud_name',
                            sortable: true,
                            width: 100
                        }, {
                            title: '列二',
                            key: 'inner_ip',
                            sortable: true
                        }, {
                            title: '列三',
                            key: 'host_name',
                            sortable: true
                        }, {
                            title: '列四',
                            key: 'date',
                            sortable: true
                        }
                    ]
                }
            },
            data: {
                default: function () {
                    return [
                        {
                            cloud_name: '华南区aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                            inner_ip: '192.168.1.1',
                            host_name: 'New York',
                            date: '2016-10-03'
                        }, {
                            cloud_name: '华南区',
                            inner_ip: '192.168.1.2',
                            host_name: 'New York',
                            date: '2016-10-04'
                        }, {
                            cloud_name: '华南区',
                            inner_ip: '192.168.1.3',
                            host_name: 'New York',
                            date: '2016-10-05'
                        }
                    ]
                }
            },
            page: {
                default: function () {
                    return {
                        page_num: 1,
                        page_size: 10,
                        total_num: 0
                    }
                }
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
            }
        },
        components: {},
        data() {
            return {
                defaultTableHeight: 100,
                columnsNew: [],
                pageData: []
            }
        },
        mounted() {
            this.defaultTableHeight = document.getElementById('cw-table-box').offsetHeight - 40;
            // this.page.page_size = parseInt((document.getElementById('cw-table-box').offsetHeight - 80) / 40);
            // this.pageSizes[0] = this.page.page_size;
            this.initColumns();
            this.initPage();
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
            }
        },
        methods: {
            initColumns() {
                let columnsNew = [];
                this.columns.forEach((item, index) => {
                    if (this.ellipsis) {
                        item['ellipsis'] = true
                    }
                    if (this.tooltip) {
                        item['tooltip'] = true
                    }
                    columnsNew.push(item);
                });
                if (columnsNew.length !== 0) {
                    this.columnsNew = columnsNew;
                } else {
                    this.columnsNew = [
                        {
                            title: '列一',
                            key: 'cloud_name',
                            sortable: true,
                            width: 100
                        }, {
                            title: '列二',
                            key: 'inner_ip',
                            sortable: true
                        }, {
                            title: '列三',
                            key: 'host_name',
                            sortable: true
                        }, {
                            title: '列四',
                            key: 'date',
                            sortable: true
                        }
                    ];
                }
            },
            initPage() {
                this.page.total_num = this.data.length;
                this.switchTablePage();
            },
            switchTablePage() {
                this.pageData = [];
                this.data.forEach((item, index) => {
                    let start = this.page.page_size * (this.page.page_num - 1);
                    let end = this.page.page_size * this.page.page_num;
                    if (start < (index + 1) && (index + 1) <= end) {
                        this.pageData.push(item);
                    }
                });
            },
            sizeChange(size) {
                if (!this.remote) {
                    this.page.page_size = size;
                    this.switchTablePage();
                } else {
                    this.$emit('sizeChange', size)
                }
            },
            currentChange(pageNum) {
                if (!this.remote) {
                    this.page.page_num = pageNum;
                    this.switchTablePage();
                } else {
                    this.$emit('currentChange', pageNum)
                }
            },
            nextClick(pageNum) {
                if (!this.remote) {
                    this.page.page_num = pageNum;
                    this.switchTablePage();
                } else {
                    this.$emit('nextClick', pageNum)
                }
            },
            prevClick(pageNum) {
                if (!this.remote) {
                    this.page.page_num = pageNum;
                    this.switchTablePage();
                } else {
                    this.$emit('prevClick', pageNum)
                }
            },
            selectCancel(selection) {
                this.$emit('on-select-cancel', selection)
            },
            selectAll(selection) {
                this.$emit('on-select-all', selection)
            },
            select(row) {
                this.$emit('on-select', row)
            }
        }
    }
</script>

<style scoped lang="scss">
    #cw-table {
        width: 100%;
        height: 100%;

        .cw-table-box {
            position: relative;
            border-right: none;

            .cw-table-footer {
                border: 1px solid #dde4eb;
                background: #fafbfd;
                height: 40px;
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
<style lang="scss">
    #cw-table {
        .ivu-table {
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
</style>
