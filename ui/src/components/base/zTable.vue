<template>
    <div>
        <Table border :columns="columns5" :data="data5" style="width: 100%">
            <template slot-scope="{ row }" slot="name">
                <strong>{{ row.name }}</strong>
            </template>
            <template slot-scope="{ row, index }" slot="action">
                <Button type="primary" size="small" style="margin-right: 5px" @click="show(index)">View</Button>
                <Button type="error" size="small" @click="remove(index)">Delete</Button>
            </template>
        </Table>
    </div>
</template>

<script>
    export default {
        name: 'zTable',
        props: {
            columns5: {
                default() {
                    return [
                        {
                            title: 'Date',
                            key: 'date',
                            sortable: true
                        },
                        {
                            title: 'Name',
                            key: 'name'
                        },
                        {
                            title: 'Age',
                            key: 'age',
                            sortable: true
                        },
                        {
                            title: 'Address',
                            key: 'address'
                        },
                        {
                            title: 'action',
                            slot: 'action'
                        }
                    ]
                },
                type: Array
            },
            data5: {
                default() {
                    return [
                        {
                            name: 'John Brown',
                            age: 18,
                            address: 'New York No. 1 Lake Park',
                            date: '2016-10-03'
                        },
                        {
                            name: 'Jim Green',
                            age: 24,
                            address: 'London No. 1 Lake Park',
                            date: '2016-10-01'
                        }
                    ]
                },
                type: Array
            }
        },
        data() {
            return {}
        }
    }
</script>

<style scoped>

</style>
