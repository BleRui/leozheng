<template>
    <div id="iView">
        <h3 class="margin-bottom10 margin-top10">选项卡</h3>
        <div class="padding-10">
            <Tabs value="tab1" :animated="false" name="tab1">
                <TabPane label="标签一1" name="tab1" tab="tab1">标签一的内容</TabPane>
                <TabPane label="标签二2" name="tab2" tab="tab1">标签二的内容</TabPane>
                <TabPane label="标签三3" name="tab3" tab="tab1">标签三的内容</TabPane>
            </Tabs>
        </div>
        <div class="padding-10" style="height: 100%;">
            <Tabs type="card" :animated="false" name="tab2" style="height: 100%;">
                <TabPane label="标签一33" name="name11" tab="tab2">标签一的内容</TabPane>
                <TabPane label="标签二33" name="name21" tab="tab2">标签二的内容</TabPane>
                <TabPane label="标签三33" name="name31" tab="tab2">标签三的内容</TabPane>
            </Tabs>
        </div>
    </div>
</template>

<script>


    export default {
        name: 'CWView',
    }
</script>

<style scoped lang="scss">
    #iView {
        padding-top: 10px;
    }
</style>
