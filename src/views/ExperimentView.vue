<template>
    <div class="experiment-start-container">
        <a-card title="开始实验">
            <p>这里是开始实验页面的内容。</p>
            <a-button type="primary">开始</a-button>
        </a-card>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { Card, Button } from '@arco-design/web-vue'; // 导入 Arco Design 组件
djfklsjdkflds
export default defineComponent({
    name: 'ExperimentStart', // 组件名称，建议与文件名一致
    components: {
        ACard: Card, // 使用 Arco Design 的 Card 组件
        AButton: Button, // 使用 Arco Design 的 Button 组件
    },
    setup() {
        // 组件的逻辑，例如数据、方法等
        return {
            // 返回模板中使用的数据或方法
        };
    },
});
</script>

<style scoped lang="less">
/* 页面的样式 */
.experiment-start-container {
    padding: 20px;
    /* 给页面内容添加一些内边距 */
}
</style>