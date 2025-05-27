<template>
    <div class="container">
        <Breadcrumb :items="['Protocol', 'Protocol.form']" />

        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t('Protocol.form.title') || '新建协议' }}
                    </template>

                    <a-row :gutter="80">
                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.protocolNo') || '协议编号'" field="protocolNo">
                                <a-input v-model="formData.protocolNo"
                                    :placeholder="$t('Protocol.form.placeholder.protocolNo') || '请输入协议编号'" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.nsn') || '国家标准编号'" field="nsn">
                                <a-input v-model="formData.nsn"
                                    :placeholder="$t('Protocol.form.placeholder.nsn') || '请输入NSN'" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.sht') || '标准加热温度'" field="sht">
                                <a-input-number v-model="formData.sht"
                                    :placeholder="$t('Protocol.form.placeholder.sht') || '请输入SHT'" :min="0"
                                    :step="0.1" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.sms') || '标准搅拌速度'" field="sms">
                                <a-input-number v-model="formData.sms"
                                    :placeholder="$t('Protocol.form.placeholder.sms') || '请输入SMS'" :min="0"
                                    :step="0.1" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-row :gutter="80">
                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.mixingAngle') || '搅拌角度'" field="mixingAngle">
                                <a-input-number v-model="formData.mixingAngle"
                                    :placeholder="$t('Protocol.form.placeholder.mixingAngle') || '请输入混合角度'" :min="0"
                                    :step="0.1" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.mixingRadius') || '标准搅拌半径'"
                                field="mixingRadius">
                                <a-input-number v-model="formData.mixingRadius"
                                    :placeholder="$t('Protocol.form.placeholder.mixingRadius') || '请输入混合半径'" :min="0"
                                    :step="0.1" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.measurementInterval') || '标准测定时间'"
                                field="measurementInterval">
                                <a-input-number v-model="formData.measurementInterval"
                                    :placeholder="$t('Protocol.form.placeholder.measurementInterval') || '请输入测量间隔'"
                                    :min="0" :step="0.1" />
                            </a-form-item>
                        </a-col>

                        <a-col :span="6">
                            <a-form-item :label="$t('Protocol.form.label.materialCode') || '材料代码'" field="materialCode">
                                <a-input v-model="formData.materialCode"
                                    :placeholder="$t('Protocol.form.placeholder.materialCode') || '请输入材料代码'" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                </a-card> </a-space>

            <div class="actions">
                <a-space>
                    <a-button @click="onResetClick">
                        {{ $t('groupForm.reset') || '重置' }}
                    </a-button>
                    <a-button type="primary" :loading="loading" @click="onSubmitClick">
                        {{ $t('groupForm.submit') || '提交' }}
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
import { useUserStore } from '@/store';

const user = useUserStore();
const formData = ref({
    protocolNo: '',
    nsn: '',
    sht: 0, // 使用 undefined 因为 input-number 初始可能为 null
    sms: 0,
    mixingAngle: 0,
    mixingRadius: 0,
    measurementInterval: 0,
    materialCode: '',
});
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
    // Write yout code here!
    const dataToSend = {
        ...formRef.value?.model, // 复制表单中已有的数据
        userName: user.userInfo.name // 添加或覆盖 userName
    };

    axios.post('/api/Protocol', dataToSend)
        .then((response) => {
            console.log(response.data);
        })
        .catch((error) => {
            console.error(error);
        });
};
const onResetClick = () => {
    formRef.value?.resetFields(); // 重置所有表单项到初始值
    // 如果你有其他需要重置的非表单绑定的数据，也可以在这里处理
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
