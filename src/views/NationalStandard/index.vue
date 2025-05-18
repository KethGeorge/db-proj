<template>
    <div class="container">
        <Breadcrumb :items="['NS', 'NS.form']" />
        <a-form ref="formRef" layout="vertical" :model="formData">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t('NS.form.title') }}
                    </template>
                    <a-form-item :label="$t('NS.form.label.name')" field="audio.approvers">
                        <a-textarea :placeholder="$t('NS.form.placeholder.name')" />
                    </a-form-item>
                    <a-form-item :label="$t('NS.form.label.description')" field="audio.approvers">
                        <a-textarea :placeholder="$t('NS.form.placeholder.description')" />
                    </a-form-item>
                </a-card>
            </a-space>
            <div class="actions">
                <a-space>
                    <a-button>
                        {{ $t('groupForm.reset') }}
                    </a-button>
                    <a-button type="primary" :loading="loading" @click="onSubmitClick">
                        {{ $t('groupForm.submit') }}
                    </a-button>
                </a-space>
            </div>
        </a-form>
    </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { FormInstance } from '@arco-design/web-vue/es/form';
import useLoading from '@/hooks/loading';

const formData = ref({});
const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();
const onSubmitClick = async () => {
    const res = await formRef.value?.validate();
    if (!res) {
        setLoading(true);
    }
    setTimeout(() => {
        setLoading(false);
    }, 1000);
};
</script>

<script lang="ts">
export default {
    name: 'NS',
};
</script>

<style scoped lang="less">
.container {
    padding: 0 20px 40px 20px;
    overflow: hidden;
}

.actions {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    height: 60px;
    padding: 14px 20px 14px 0;
    background: var(--color-bg-2);
    text-align: right;
}
</style>
