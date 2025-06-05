<!-- <template>
    <div class="container">
        <Breadcrumb :items="['Mat', 'Mat.form']" />
        <a-form ref="formRef" layout="vertical" :model="formData">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t('Mat.form.title') }}
                    </template>
                    <a-form-item :label="$t('Mat.form.label.name')" field="audio.approvers">
                        <a-textarea :placeholder="$t('Mat.form.placeholder.name')" />
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
</template> -->

<template>
    <div class="container">
        <Breadcrumb :items="['Mat', 'Mat.form']" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t('Mat.form.title') }}
                    </template>
                    <a-form-item :label="$t('Mat.form.label.name')" field="name">
                        <a-textarea v-model="formData.name" :placeholder="$t('Mat.form.placeholder.name')" />
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
import axios from 'axios';

const formData = ref({name: ''});
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
    axios.post('/api/Mat', formRef.value?.model)
        .then((response) => {
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
        });
};
</script>

<script lang="ts">
export default {
    name: 'Mat',
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
