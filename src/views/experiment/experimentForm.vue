<template>
    <div class="container">
        <Breadcrumb
            :items="['Experiment', isCreate ? 'experiment.form.title.create' : (isEdit ? 'experiment.form.title.edit' : 'experiment.form.title.view')]" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t(formTitle) }}
                    </template>
                    <a-row :gutter="16">
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.ExperimentNo')" field="ExperimentNo"
                                :rules="[{ required: true, message: $t('experiment.form.validation.ExperimentNoRequired') }, { min:1, max:16, message: $t('experiment.form.validation.ExperimentNoLength') }]"
                                >
                                <a-input v-model="formData.ExperimentNo" :placeholder="$t('experiment.form.placeholder.ExperimentNo')"
                                    :disabled="!isCreate" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.MaterialCode')" field="MaterialCode"
                                :rules="[{ max:16, message: $t('experiment.form.validation.MaterialCodeLength') }]">
                                <a-input v-model="materialCodeComputed"
                                    :placeholder="$t('experiment.form.placeholder.MaterialCode')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.ProtocolNo')" field="ProtocolNo"
                                :rules="[{ max:8, message: $t('experiment.form.validation.ProtocolNoLength') }]">
                                <a-input v-model="protocolNoComputed"
                                    :placeholder="$t('experiment.form.placeholder.ProtocolNo')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-row :gutter="16">
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.UserNo')" field="UserNo"
                                :rules="[{ required: true, message: $t('experiment.form.validation.UserNoRequired') }, { min:1, max:8, message: $t('experiment.form.validation.UserNoLength') }]">
                                <a-input v-model="formData.UserNo"
                                    :placeholder="$t('experiment.form.placeholder.UserNo')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.HeatError')" field="HeatError"
                                :rules="[{ type: 'number', message: $t('experiment.form.validation.HeatErrorNumber') }]">
                                <a-input-number
                                    v-model="heatErrorComputed"
                                    :placeholder="$t('experiment.form.placeholder.HeatError')"
                                    :disabled="!isEdit && !isCreate" :step="0.01" allow-clear />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.MixError')" field="MixError"
                                :rules="[{ type: 'number', message: $t('experiment.form.validation.MixErrorNumber') }]">
                                <a-input-number
                                    v-model="mixErrorComputed"
                                    :placeholder="$t('experiment.form.placeholder.MixError')"
                                    :disabled="!isEdit && !isCreate" :step="0.01" allow-clear />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-row :gutter="16">
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.StartTime')" field="StartTime"
                                :rules="[{ required: true, message: $t('experiment.form.validation.StartTimeRequired') }]">
                                <a-time-picker
                                    v-model="startTimeComputed"
                                    :placeholder="$t('experiment.form.placeholder.StartTime')"
                                    :disabled="!isEdit && !isCreate"
                                    format="HH:mm:ss"
                                    value-format="HH:mm:ss" allow-clear />
                            </a-form-item>
                        </a-col>
                        <a-col :span="8">
                            <a-form-item :label="$t('experiment.form.label.EndTime')" field="EndTime"
                                :rules="[{ required: true, message: $t('experiment.form.validation.EndTimeRequired') }]">
                                <a-time-picker
                                    v-model="endTimeComputed"
                                    :placeholder="$t('experiment.form.placeholder.EndTime')"
                                    :disabled="!isEdit && !isCreate"
                                    format="HH:mm:ss"
                                    value-format="HH:mm:ss" allow-clear />
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
import { queryExperimentDetail, createExperiment, updateExperimentInfo, ExperimentRecord } from '@/api/experiment';
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';
import cloneDeep from 'lodash/cloneDeep';

const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();
const route = useRoute();
const router = useRouter();
const { t } = useI18n();

const formData = reactive<ExperimentRecord>({
    ExperimentNo: '',
    MaterialCode: undefined,
    HeatError: undefined,
    MixError: undefined,
    StartTime: undefined,
    EndTime: undefined,
    ProtocolNo: undefined,
    UserNo: '',
});

const experimentNoFromRoute = computed(() => route.params.experimentNo as string | undefined);
const isCreate = computed(() => route.name === 'ExperimentAdminCreate');
const isEdit = computed(() => route.name === 'ExperimentAdminEdit');
const isView = computed(() => route.name === 'ExperimentAdminView');

const formTitle = computed(() => {
    if (isCreate.value) return 'experiment.form.title.create';
    if (isEdit.value) return 'experiment.form.title.edit';
    if (isView.value) return 'experiment.form.title.view';
    return 'experiment.form.title.default';
});

// 泛型计算属性工厂，处理 number | null | undefined 类型
const createNumberComputed = (key: 'HeatError' | 'MixError') => computed({
  get: () => {
    const value = formData[key];
    return value === null ? undefined : (value as number | undefined);
  },
  set: (value: number | undefined) => {
    (formData[key] as number | null | undefined) = value === undefined ? null : value;
  }
});

const heatErrorComputed = createNumberComputed('HeatError');
const mixErrorComputed = createNumberComputed('MixError');

// 泛型计算属性工厂，处理 string | null | undefined 类型 (用于 a-input)
const createStringComputed = (key: 'MaterialCode' | 'ProtocolNo') => computed({
  get: () => {
    const value = formData[key];
    return value === null ? undefined : (value as string | undefined);
  },
  set: (value: string | undefined) => {
    (formData[key] as string | null | undefined) = (value === undefined || value === '') ? null : value;
  }
});

const materialCodeComputed = createStringComputed('MaterialCode');
const protocolNoComputed = createStringComputed('ProtocolNo');


// 泛型计算属性工厂，用于 a-time-picker 的双向绑定，处理 null/undefined/'' 转换
const createTimeComputed = (key: 'StartTime' | 'EndTime') => computed({
  get: () => {
    const value = formData[key];
    return value === null ? undefined : (value as string | undefined);
  },
  set: (value: string | undefined) => {
    formData[key] = (value === undefined || value === '') ? null : value;
  }
});

const startTimeComputed = createTimeComputed('StartTime');
const endTimeComputed = createTimeComputed('EndTime');


// 获取协议详情数据
const fetchExperimentData = async (experimentNo: string) => {
    setLoading(true);
    try {
        const res = await queryExperimentDetail(experimentNo);
        Object.assign(formData, res);
    } catch (error: any) {
        Message.error(`${t('experiment.message.fetchFail')}: ${error.message || '未知错误'}`);
        console.error('Error fetching experiment data:', error);
        router.back();
    } finally {
        setLoading(false);
    }
};

const resetForm = () => {
    Object.assign(formData, {
        ExperimentNo: '',
        MaterialCode: undefined,
        HeatError: undefined,
        MixError: undefined,
        StartTime: undefined,
        EndTime: undefined,
        ProtocolNo: undefined,
        UserNo: '',
    });
    formRef.value?.resetFields();
};

watch(
    () => route.params.experimentNo,
    (newVal) => {
        if ((isEdit.value || isView.value) && newVal) {
            fetchExperimentData(newVal as string);
        } else if (isCreate.value) {
            resetForm();
        }
    },
    { immediate: true }
);

onMounted(() => {
    if ((isEdit.value || isView.value) && experimentNoFromRoute.value) {
        fetchExperimentData(experimentNoFromRoute.value);
    }
});

const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
        setLoading(true);
        try {
            const dataToSend: Partial<ExperimentRecord> = cloneDeep(formData);

            // 统一处理可能为空的字段：将 undefined 或 '' 转换为 null
            const nullableStringFields: (keyof ExperimentRecord)[] = ['MaterialCode', 'ProtocolNo'];
            nullableStringFields.forEach(key => {
                const value = dataToSend[key];
                if (value === undefined || value === '') {
                    (dataToSend as any)[key] = null;
                }
            });

            const nullableNumberFields: (keyof ExperimentRecord)[] = ['HeatError', 'MixError'];
            nullableNumberFields.forEach(key => {
                const value = dataToSend[key];
                if (value === undefined || value === '') {
                    (dataToSend as any)[key] = null;
                }
            });

            const nullableTimeFields: (keyof ExperimentRecord)[] = ['StartTime', 'EndTime'];
            nullableTimeFields.forEach(key => {
                const value = dataToSend[key];
                if (value === undefined) {
                    (dataToSend as any)[key] = null;
                }
            });


            if (isCreate.value) {
                await createExperiment(dataToSend as ExperimentRecord);
                Message.success(t('experiment.message.createSuccess'));
                router.push({ name: 'ExperimentAdminList' });
            } else if (isEdit.value) {
                if (!experimentNoFromRoute.value) {
                    Message.error(t('experiment.message.idMissingForUpdate'));
                    setLoading(false);
                    return;
                }
                await updateExperimentInfo(experimentNoFromRoute.value, dataToSend);
                Message.success(t('experiment.message.updateSuccess'));
                router.push({ name: 'ExperimentAdminList' });
            }

        } catch (error: any) {
            console.error('提交实验信息失败:', error);
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
    name: 'ExperimentForm',
};
</script>

<style scoped lang="less">
.container {
    padding: 0 20px 40px 20px;
}

:deep(.arco-select-view-disabled),
:deep(.arco-input-disabled),
:deep(.arco-textarea-disabled),
:deep(.arco-input-number-disabled),
:deep(.arco-picker-disabled) {
    background-color: var(--color-bg-2)!important;
    border-color: var(--color-border-2)!important;
    cursor: default!important;
    pointer-events: none!important;
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