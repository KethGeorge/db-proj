<template>
    <div class="container">
        <Breadcrumb
            :items="['Material', isCreate ? 'material.form.title.create' : (isEdit ? 'material.form.title.edit' : 'material.form.title.view')]" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t(formTitle) }}
                    </template>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('material.form.label.MaterialCode')" field="MaterialCode"
                                :rules="[{ required: true, message: $t('material.form.validation.MaterialCodeRequired') }, { min: 1, max: 16, message: $t('material.form.validation.MaterialCodeLength') }]">
                                <a-input v-model="formData.MaterialCode"
                                    :placeholder="$t('material.form.placeholder.MaterialCode')" :disabled="!isCreate" />
                                <!-- MaterialCode 仅在创建时可编辑 -->
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item :label="$t('material.form.label.MaterialName')" field="MaterialName"
                                :rules="[{ required: true, message: $t('material.form.validation.MaterialNameRequired') }, { min: 1, max: 20, message: $t('material.form.validation.MaterialNameLength') }]">
                                <a-input v-model="formData.MaterialName"
                                    :placeholder="$t('material.form.placeholder.MaterialName')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <!-- 如果 Material 表有更多字段，可以在这里添加 -->

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
import { queryMaterialDetail, createMaterial, updateMaterialInfo, MaterialRecord } from '@/api/materials'; // 导入新的API
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n'; // 导入 useI18n

const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();
const route = useRoute();
const router = useRouter();
const { t } = useI18n(); // 使用国际化

const formData = reactive<MaterialRecord>({
    MaterialCode: '',
    MaterialName: '',
});

const materialCodeFromRoute = computed(() => route.params.materialCode as string | undefined);
const isCreate = computed(() => route.name === 'MaterialAdminCreate');
const isEdit = computed(() => route.name === 'MaterialAdminEdit');
const isView = computed(() => route.name === 'MaterialAdminView');

const formTitle = computed(() => {
    if (isCreate.value) return 'material.form.title.create';
    if (isEdit.value) return 'material.form.title.edit';
    if (isView.value) return 'material.form.title.view';
    return 'material.form.title.default';
});

// 获取材料详情数据
const fetchMaterialData = async (materialCode: string) => {
    setLoading(true);
    try {
        const res = await queryMaterialDetail(materialCode);
        // 填充表单数据
        formData.MaterialCode = res.MaterialCode;
        formData.MaterialName = res.MaterialName;

    } catch (error: any) {
        Message.error(`${t('material.message.fetchFail')}: ${error.message || '未知错误'}`);
        console.error('Error fetching material data:', error);
        router.back();
    } finally {
        setLoading(false);
    }
};

const resetForm = () => {
    if (isCreate.value) {
        Object.assign(formData, {
            MaterialCode: '',
            MaterialName: '',
        });
        formRef.value?.resetFields();
    } else if (materialCodeFromRoute.value) {
        fetchMaterialData(materialCodeFromRoute.value);
    }

};

watch(
    () => route.params.materialCode,
    (newVal) => {
        if ((isEdit.value || isView.value) && newVal) {
            fetchMaterialData(newVal as string);
        } else if (isCreate.value) {
            resetForm();
        }
    },
    { immediate: true }
);

onMounted(() => {
    if ((isEdit.value || isView.value) && materialCodeFromRoute.value) {
        fetchMaterialData(materialCodeFromRoute.value);
    }
});

const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
        setLoading(true);
        try {
            const dataToSend: MaterialRecord = {
                MaterialCode: formData.MaterialCode,
                MaterialName: formData.MaterialName,
            };

            if (isCreate.value) {
                await createMaterial(dataToSend);
                Message.success(t('material.message.createSuccess'));
                router.push({ name: 'MaterialAdminList' });
            } else if (isEdit.value) {
                if (!materialCodeFromRoute.value) {
                    Message.error(t('material.message.idMissingForUpdate'));
                    setLoading(false);
                    return;
                }
                await updateMaterialInfo(materialCodeFromRoute.value, dataToSend);
                Message.success(t('material.message.updateSuccess'));
                router.push({ name: 'MaterialAdminList' });
            }

        } catch (error: any) {
            console.error('提交材料信息失败:', error);
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
    name: 'MaterialForm',
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