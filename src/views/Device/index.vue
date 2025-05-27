<template>
    <div class="container">
        <Breadcrumb :items="['Device', 'Device.form']" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t('device.form.title') }}
                    </template>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.deviceNo')" field="deviceNo"
                                :rules="[{ required: true, message: '设备编号不能为空' }]">
                                <a-input v-model="formData.deviceNo"
                                    :placeholder="$t('device.form.placeholder.deviceNo')" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item :label="$t('device.form.label.deviceName')" field="deviceName"
                                :rules="[{ required: true, message: '设备名称不能为空' }]">
                                <a-input v-model="formData.deviceName"
                                    :placeholder="$t('device.form.placeholder.deviceName')" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-form-item :label="$t('device.form.label.deviceUsage')" field="deviceUsage">
                        <a-textarea v-model="formData.deviceUsage"
                            :placeholder="$t('device.form.placeholder.deviceUsage')"
                            :auto-size="{ minRows: 2, maxRows: 4 }" />
                    </a-form-item>

                    <a-form-item :label="$t('device.form.label.dStartTime')" field="dStartTime">
                        <a-checkbox v-model="formData.dStartTime_disabled" class="date-time-checkbox">
                            {{ $t('device.form.label.disableDateTime') }}
                        </a-checkbox>
                        <a-row :gutter="8" :class="{ 'disabled-row': formData.dStartTime_disabled }">
                            <a-col :span="12">
                                <a-date-picker v-model="formData.dStartTime_date" style="width: 100%;"
                                    :placeholder="$t('device.form.placeholder.dStartTimeDate')"
                                    :disabled="formData.dStartTime_disabled" />
                            </a-col>
                            <a-col :span="12">
                                <a-time-picker v-model="formData.dStartTime_time" style="width: 100%;" format="HH:mm:ss"
                                    :placeholder="$t('device.form.placeholder.dStartTimeTime')"
                                    :disabled="formData.dStartTime_disabled" />
                            </a-col>
                        </a-row>
                    </a-form-item>

                    <a-form-item :label="$t('device.form.label.dmt')" field="dmt">
                        <a-checkbox v-model="formData.dmt_disabled" class="date-time-checkbox">
                            {{ $t('device.form.label.disableDateTime') }}
                        </a-checkbox>
                        <a-row :gutter="8" :class="{ 'disabled-row': formData.dmt_disabled }">
                            <a-col :span="12">
                                <a-date-picker v-model="formData.dmt_date" style="width: 100%;"
                                    :placeholder="$t('device.form.placeholder.dmtDate')"
                                    :disabled="formData.dmt_disabled" />
                            </a-col>
                            <a-col :span="12">
                                <a-time-picker v-model="formData.dmt_time" style="width: 100%;" format="HH:mm:ss"
                                    :placeholder="$t('device.form.placeholder.dmtTime')"
                                    :disabled="formData.dmt_disabled" />
                            </a-col>
                        </a-row>
                    </a-form-item>

                    <a-form-item :label="$t('device.form.label.dStopTime')" field="dStopTime">
                        <a-checkbox v-model="formData.dStopTime_disabled" class="date-time-checkbox">
                            {{ $t('device.form.label.disableDateTime') }}
                        </a-checkbox>
                        <a-row :gutter="8" :class="{ 'disabled-row': formData.dStopTime_disabled }">
                            <a-col :span="12">
                                <a-date-picker v-model="formData.dStopTime_date" style="width: 100%;"
                                    :placeholder="$t('device.form.placeholder.dStopTimeDate')"
                                    :disabled="formData.dStopTime_disabled" />
                            </a-col>
                            <a-col :span="12">
                                <a-time-picker v-model="formData.dStopTime_time" style="width: 100%;" format="HH:mm:ss"
                                    :placeholder="$t('device.form.placeholder.dStopTimeTime')"
                                    :disabled="formData.dStopTime_disabled" />
                            </a-col>
                        </a-row>
                    </a-form-item>

                </a-card>
            </a-space>
            <div class="actions">
                <a-space>
                    <a-button @click="resetForm">
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
import { ref, reactive } from 'vue';
import { FormInstance } from '@arco-design/web-vue/es/form';
import { Message } from '@arco-design/web-vue';
import useLoading from '@/hooks/loading';
import axios, { AxiosResponse }  from 'axios';
import { useUserStore } from '@/store';

const user = useUserStore();
const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();

// 定义表单数据结构
const formData = reactive({
    deviceNo: '',
    deviceName: '',
    deviceUsage: '',
    // DStartTime 相关
    dStartTime_disabled: false,
    dStartTime_date: undefined as Date | undefined, // undefined 可以更好地表示未选择
    dStartTime_time: '' as string, // 字符串 'HH:mm:ss'

    // DMT 相关
    dmt_disabled: false,
    dmt_date: undefined as Date | undefined,
    dmt_time: '' as string,

    // DStopTime 相关
    dStopTime_disabled: false,
    dStopTime_date: undefined as Date | undefined,
    dStopTime_time: '' as string,
});

// 辅助函数：将 Date 和时间字符串合并为 ISO 字符串
const combineDateTime = (dateObj: Date | undefined, timeStr: string): string | null => {
    if (!dateObj) {
        return null;
    }

    // *** 关键检查：确保 dateObj 是一个 Date 实例 ***
    if (!(dateObj instanceof Date)) {
        console.warn("combineDateTime 收到一个非 Date 对象，尝试转换为 Date:", dateObj);
        // 如果 dateObj 是一个有效的日期字符串，可以尝试转换
        try {
            const parsedDate = new Date(dateObj);
            if (!Number.isNaN(parsedDate.getTime())) { // 检查是否是有效日期
                dateObj = parsedDate;
            } else {
                console.error("combineDateTime 无法将非 Date 对象转换为有效日期:", dateObj);
                return null; // 无法转换，返回 null
            }
        } catch (e) {
            console.error("combineDateTime 转换日期时发生错误:", e);
            return null;
        }
    }


    const year = dateObj.getFullYear();
    const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
    const day = dateObj.getDate().toString().padStart(2, '0');

    // 默认时间为 '00:00:00' 如果 timeStr 为空
    const timePart = timeStr || '00:00:00';

    // 组合成一个标准日期时间字符串，如 'YYYY-MM-DDTHH:mm:ss'
    return `${year}-${month}-${day}T${timePart}`;
};
// 定义一个接口来描述后端 API 响应的结构
interface ApiResponse<T = any> {
    code: number;
    message: string;
    data: T; // 这里 T 是业务数据的类型，例如 { deviceName: string; deviceNo: string; }
}
const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();

    if (!errors) {
        setLoading(true);
        try {
            const dataToSend: { [key: string]: any } = {
                deviceNo: formData.deviceNo,
                deviceName: formData.deviceName,
                deviceUsage: formData.deviceUsage,
                operator: user.userInfo.name || 'unknown_user',
            };

            // ---- 关键修改部分 ----

            // ---- 结束修改部分 ----

            // 处理 DStartTime
            let dStartTimeDateObj: Date | undefined;
            if (formData.dStartTime_date instanceof Date) {
                dStartTimeDateObj = formData.dStartTime_date;
            } else if (formData.dStartTime_date) { // 如果不是 Date 对象但有值（可能是字符串）
                const parsedDate = new Date(formData.dStartTime_date);
                dStartTimeDateObj = Number.isNaN(parsedDate.getTime()) ? undefined : parsedDate;
            } else {
                dStartTimeDateObj = undefined; // 明确为 undefined
            }

            let dmtDateObj: Date | undefined;
            if (formData.dmt_date instanceof Date) {
                dmtDateObj = formData.dmt_date;
            } else if (formData.dmt_date) {
                const parsedDate = new Date(formData.dmt_date);
                dmtDateObj = Number.isNaN(parsedDate.getTime()) ? undefined : parsedDate;
            } else {
                dmtDateObj = undefined;
            }

            let dStopTimeDateObj: Date | undefined;
            if (formData.dStopTime_date instanceof Date) {
                dStopTimeDateObj = formData.dStopTime_date;
            } else if (formData.dStopTime_date) {
                const parsedDate = new Date(formData.dStopTime_date);
                dStopTimeDateObj = Number.isNaN(parsedDate.getTime()) ? undefined : parsedDate;
            } else {
                dStopTimeDateObj = undefined;
            }

            const response: ApiResponse<{ deviceName: string; deviceNo: string; }> = await axios.post('/api/device', dataToSend);

            console.log('完整的 Axios 响应对象:', response); // AxiosResponse 实例
            console.log('后端返回的实际数据 (response.data):', response.data); // 后端返回的 JSON 对象 { code, message, data }

            // 访问后端返回的 code 和 message 都在 response.data 里面
            if (response.data && response.code === 20000) {
                Message.success(response.message || '设备信息提交成功！');
                resetForm();
            } else {
                // 如果后端返回的 code 不是 20000，显示错误信息
                Message.error(response.message || '设备信息提交失败！');
            }
        } catch (error) {
            console.error('提交设备信息失败:', error);
            if (axios.isAxiosError(error) && error.response) {
                Message.error(`提交失败: ${error.response.data.message || error.response.statusText}`);
            } else {
                Message.error('网络或服务器错误，请稍后再试。');
            }
        } finally {
            setLoading(false);
        }
    } else {
        Message.warning('请检查并填写所有必填项！');
    }
};

const resetForm = () => {
    // 重置所有表单字段
    Object.assign(formData, {
        deviceNo: '',
        deviceName: '',
        deviceUsage: '',
        dStartTime_disabled: false,
        dStartTime_date: undefined, // 重置为 undefined
        dStartTime_time: '',
        dmt_disabled: false,
        dmt_date: undefined,
        dmt_time: '',
        dStopTime_disabled: false,
        dStopTime_date: undefined,
        dStopTime_time: '',
    });
    formRef.value?.resetFields();
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

.date-time-checkbox {
    margin-bottom: 8px;
    margin-right: 16px;
    vertical-align: middle;
}

.disabled-row {
    opacity: 0.6;
    pointer-events: none;
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