<template>
    <div class="container">
        <Breadcrumb
            :items="['Device', isCreate ? 'device.form.title.create' : (isEdit ? 'device.form.title.edit' : 'device.form.title.view')]" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t(formTitle) }}
                    </template>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.DeviceNo')" field="DeviceNo"
                                :rules="[{ required: true, message: $t('device.form.validation.DeviceNoRequired') }, { min: 1, max: 20, message: $t('device.form.validation.DeviceNoLength') }]">
                                <a-input v-model="formData.DeviceNo"
                                    :placeholder="$t('device.form.placeholder.DeviceNo')" :disabled="!isCreate" />
                                <!-- DeviceNo 仅在创建时可编辑 -->
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.DeviceName')" field="DeviceName"
                                :rules="[{ required: true, message: $t('device.form.validation.DeviceNameRequired') }, { min: 1, max: 8, message: $t('device.form.validation.DeviceNameLength') }]">
                                <a-input v-model="formData.DeviceName"
                                    :placeholder="$t('device.form.placeholder.DeviceName')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.DeviceUsage')" field="DeviceUsage"
                                :rules="[{ max: 10, message: $t('device.form.validation.DeviceUsageLength') }]">
                                <a-input v-model="formData.DeviceUsage"
                                    :placeholder="$t('device.form.placeholder.DeviceUsage')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                        <!-- <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.Operator')" field="Operator">
                                <a-input v-model="formData.Operator"
                                    :placeholder="$t('device.form.placeholder.Operator')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col> -->
                    </a-row>

                    <!-- 时间字段 -->
                    <a-row :gutter="16">
                        <a-col :span="8">
                            <a-form-item :label="$t('device.form.label.DStartTime')" field="DStartTime">
                                <a-date-picker show-time style="width: 100%" v-model="formData.DStartTime"
                                    :placeholder="$t('device.form.placeholder.DStartTime')"
                                    :disabled="!isEdit && !isCreate" value-format="YYYY-MM-DDTHH:mm:ss" />
                                <!-- 后端需要ISO格式 -->
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('device.form.label.DMT')" field="DMT">
                                <a-date-picker show-time style="width: 100%" v-model="formData.DMT"
                                    :placeholder="$t('device.form.placeholder.DMT')" :disabled="!isEdit && !isCreate"
                                    value-format="YYYY-MM-DDTHH:mm:ss" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('device.form.label.DStopTime')" field="DStopTime">
                                <a-date-picker show-time style="width: 100%" v-model="formData.DStopTime"
                                    :placeholder="$t('device.form.placeholder.DStopTime')"
                                    :disabled="!isEdit && !isCreate" value-format="YYYY-MM-DDTHH:mm:ss" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                </a-card>
            </a-space>
            <div class="actions">
                <a-space>
                    <a-button v-if="isEdit || isCreate" @click="resetForm">
                        {{ $t('groupForm.reset') }}
                    </a-button>
                    <a-button type="primary" :loading="loading" @click="onSubmitClick" v-if="isEdit || isCreate">
                        {{ isCreate ? $t('groupForm.submit') : $t('groupForm.save') }}
                    </a-button>
                    <a-button type="primary" @click="goBack">
                        {{ $t('groupForm.back') }}
                    </a-button>
                </a-space>
            </div>
        </a-form>
    </div>
</template>

<script lang="ts" setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { FormInstance } from '@arco-design/web-vue/es/form';
import { Message } from '@arco-design/web-vue';
import useLoading from '@/hooks/loading';
import { queryDeviceDetail, createDevice, updateDeviceInfo, DeviceRecord } from '@/api/device'; // 导入新的API
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();
const route = useRoute();
const router = useRouter();
const { t } = useI18n();

const formData = reactive<DeviceRecord>({
    DeviceNo: '',
    DeviceName: '',
    DeviceUsage: '',
    DStartTime: undefined, // 初始化为 undefined 或 null
    DMT: undefined,
    DStopTime: undefined,
    // Operator: '',
});

const deviceNoFromRoute = computed(() => route.params.deviceNo as string | undefined);
const isCreate = computed(() => route.name === 'DeviceAdminCreate');
const isEdit = computed(() => route.name === 'DeviceAdminEdit');
const isView = computed(() => route.name === 'DeviceAdminView');

const formTitle = computed(() => {
    if (isCreate.value) return 'device.form.title.create';
    if (isEdit.value) return 'device.form.title.edit';
    if (isView.value) return 'device.form.title.view';
    return 'device.form.title.default';
});

// 获取设备详情数据
const fetchDeviceData = async (deviceNo: string) => {
    setLoading(true);
    try {
        const res = await queryDeviceDetail(deviceNo);
        // 填充表单数据
        Object.assign(formData, res); // 直接合并后端返回的数据
    } catch (error: any) {
        Message.error(`${t('device.message.fetchFail')}: ${error.message || '未知错误'}`);
        console.error('Error fetching device data:', error);
        router.back();
    } finally {
        setLoading(false);
    }
};

const resetForm = () => {
    if (isCreate.value) {
        Object.assign(formData, {
            DeviceNo: '',
            DeviceName: '',
            DeviceUsage: '',
            DStartTime: undefined,
            DMT: undefined,
            DStopTime: undefined,
            Operator: '',
        });
        formRef.value?.resetFields();
    } else 
        if (deviceNoFromRoute.value) {
            fetchDeviceData(deviceNoFromRoute.value);
        }
    
};

watch(
    () => route.params.deviceNo,
    (newVal) => {
        if ((isEdit.value || isView.value) && newVal) {
            fetchDeviceData(newVal as string);
        } else if (isCreate.value) {
            resetForm();
        }
    },
    { immediate: true }
);

onMounted(() => {
    if ((isEdit.value || isView.value) && deviceNoFromRoute.value) {
        fetchDeviceData(deviceNoFromRoute.value);
    }
});

const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
        setLoading(true);
        try {
            const dataToSend: DeviceRecord = { ...formData }; // 创建副本以发送

            // 确保日期时间字段为 null 而不是空字符串
            ['DStartTime', 'DMT', 'DStopTime'].forEach(key => {
                if (dataToSend[key as keyof DeviceRecord] === '') {
                    (dataToSend as any)[key] = null;
                }
            });

            if (isCreate.value) {
                await createDevice(dataToSend);
                Message.success(t('device.message.createSuccess'));
                router.push({ name: 'DeviceAdminList' });
            } else if (isEdit.value) {
                if (!deviceNoFromRoute.value) {
                    Message.error(t('device.message.idMissingForUpdate'));
                    setLoading(false);
                    return;
                }
                await updateDeviceInfo(deviceNoFromRoute.value, dataToSend);
                Message.success(t('device.message.updateSuccess'));
                router.push({ name: 'DeviceAdminList' });
            } 

        } catch (error: any) {
            console.error('提交设备信息失败:', error);
            Message.error(`${t('groupForm.operationFail')}: ${error.message || '未知错误'}`);
        } finally {
            setLoading(false);
        }
    } else {
        Message.warning(t('groupForm.validationWarning'));
    }
};

const goBack = () => {
    router.back();
};

</script>

<script lang="ts">
export default {
    name: 'DeviceForm',
};
</script>

<style scoped lang="less">
.container {
    padding: 0 20px 40px 20px;
    overflow: hidden;
}

:deep(.arco-select-view-disabled),
:deep(.arco-input-disabled),
:deep(.arco-textarea-disabled) {
    background-color: var(--color-bg-2) !important;
    border-color: var(--color-border-2) !important;
    cursor: default !important;
    pointer-events: none !important;
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
    box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
}
</style>