<template>
  <div class="container">
    <Breadcrumb
      :items="[
        'NationalStandard',
        isCreate
          ? 'nationalStandard.form.title.create'
          : isEdit
          ? 'nationalStandard.form.title.edit'
          : 'nationalStandard.form.title.view',
      ]"
    />
    <a-form
      ref="formRef"
      layout="vertical"
      :model="formData"
      @submit="onSubmitClick"
    >
      <a-space direction="vertical" :size="16">
        <a-card class="general-card" :bordered="false">
          <template #title>
            {{ $t(formTitle) }}
          </template>
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                :label="$t('nationalStandard.form.label.NSN')"
                field="NSN"
                :rules="[
                  {
                    required: true,
                    message: $t('nationalStandard.form.validation.NSNRequired'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.NSN"
                  :placeholder="$t('nationalStandard.form.placeholder.NSN')"
                  :disabled="!isCreate"
                />
                <!-- NSN 仅在创建时可编辑 -->
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('nationalStandard.form.label.StandardName')"
                field="StandardName"
                :rules="[
                  {
                    required: true,
                    message: $t(
                      'nationalStandard.form.validation.StandardNameRequired'
                    ),
                  },
                ]"
              >
                <a-input
                  v-model="formData.StandardName"
                  :placeholder="
                    $t('nationalStandard.form.placeholder.StandardName')
                  "
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                :label="$t('nationalStandard.form.label.MaterialCode')"
                field="MaterialCode"
              >
                <a-input
                  v-model="formData.MaterialCode"
                  :placeholder="
                    $t('nationalStandard.form.placeholder.MaterialCode')
                  "
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
            <!-- 可以添加其他字段，例如 Description 的 Textarea -->
            <a-col :span="12">
              <a-form-item
                :label="$t('nationalStandard.form.label.Description')"
                field="Description"
              >
                <a-textarea
                  v-model="formData.Description"
                  :placeholder="
                    $t('nationalStandard.form.placeholder.Description')
                  "
                  :disabled="!isEdit && !isCreate"
                  :auto-size="{ minRows: 2, maxRows: 5 }"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <!-- 其他字段可以按需添加，例如分类、发布日期等 -->
        </a-card>
      </a-space>
      <div class="actions">
        <a-space>
          <a-button v-if="isEdit || isCreate" @click="resetForm">
            {{ $t('groupForm.reset') }}
          </a-button>
          <a-button
            v-if="isEdit || isCreate"
            type="primary"
            :loading="loading"
            @click="onSubmitClick"
          >
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
  import { FormInstance, Message } from '@arco-design/web-vue';
  import useLoading from '@/hooks/loading';
  // 导入统一管理后的 API 函数
  import {
    queryNationalStandardDetail,
    createNationalStandard,
    updateNationalStandardInfo,
    NationalStandardRecord,
  } from '@/api/NationalStandard';
  import { useRoute, useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';

  const { t } = useI18n();
  const formRef = ref<FormInstance>();
  const { loading, setLoading } = useLoading();
  const route = useRoute();
  const router = useRouter();

  const formData = reactive<NationalStandardRecord>({
    NSN: '',
    StandardName: '',
    Description: '',
    MaterialCode: '',
  });

  const nsnFromRoute = computed(() => route.params.nsn as string | undefined);
  const isCreate = computed(() => route.name === 'NationalStandardAdminCreate');
  const isEdit = computed(() => route.name === 'NationalStandardAdminEdit');
  const isView = computed(() => route.name === 'NationalStandardAdminView');

  const formTitle = computed(() => {
    if (isCreate.value) return 'nationalStandard.form.title.create';
    if (isEdit.value) return 'nationalStandard.form.title.edit';
    if (isView.value) return 'nationalStandard.form.title.view';
    return 'nationalStandard.form.title.default';
  });

  // 获取国家标准详情数据
  const fetchStandardData = async (nsn: string) => {
    setLoading(true);
    try {
      const res = await queryNationalStandardDetail(nsn);

      // 填充表单数据
      formData.NSN = res.NSN;
      formData.StandardName = res.StandardName;
      formData.Description = res.Description;
      formData.MaterialCode = res.MaterialCode;
    } catch (error: any) {
      Message.error(
        `${t('nationalStandard.message.fetchFail')}: ${
          error.message || '未知错误'
        }`
      );
      console.error('Error fetching standard data:', error);
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    // 仅在创建模式下才完全重置
    if (isCreate.value) {
      Object.assign(formData, {
        NSN: '',
        StandardName: '',
        Description: '',
        MaterialCode: '',
      });
      formRef.value?.resetFields();
    } else if (nsnFromRoute.value) {
      // 编辑或查看模式，重新加载数据以回到原始状态

      fetchStandardData(nsnFromRoute.value);
    }
  };

  // 监听路由参数变化，如果是编辑或查看模式则重新加载数据
  watch(
    () => route.params.nsn,
    (newVal) => {
      if ((isEdit.value || isView.value) && newVal) {
        fetchStandardData(newVal as string);
      } else if (isCreate.value) {
        resetForm(); // 如果是创建模式，确保表单是空的
      }
    },
    { immediate: true } // 立即执行一次，以防组件在路由加载时就已经渲染
  );

  // 初始化时，如果当前是编辑或查看模式，且nsn已存在，则加载数据
  onMounted(() => {
    if ((isEdit.value || isView.value) && nsnFromRoute.value) {
      fetchStandardData(nsnFromRoute.value);
    }
  });

  const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
      setLoading(true);
      try {
        let res;
        const dataToSend: NationalStandardRecord = {
          NSN: formData.NSN,
          StandardName: formData.StandardName,
          Description: formData.Description,
          MaterialCode: formData.MaterialCode,
        };

        if (isCreate.value) {
          res = await createNationalStandard(dataToSend);
          Message.success(t('nationalStandard.message.createSuccess'));
          router.push({ name: 'NationalStandardAdminList' }); // 创建成功后返回列表页
        } else if (isEdit.value) {
          if (!nsnFromRoute.value) {
            Message.error(t('nationalStandard.message.idMissingForUpdate'));
            setLoading(false);
            return;
          }
          res = await updateNationalStandardInfo(
            nsnFromRoute.value,
            dataToSend
          );
          Message.success(t('nationalStandard.message.updateSuccess'));
          router.push({ name: 'NationalStandardAdminList' }); // 更新成功后返回列表页
        }
      } catch (error: any) {
        console.error('提交国家标准信息失败:', error);
        Message.error(
          `${t('groupForm.operationFail')}: ${error.message || '未知错误'}`
        );
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
    name: 'NationalStandardForm',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 40px;
    overflow: hidden;
  }

  .date-time-checkbox {
    margin-right: 16px;
    margin-bottom: 8px;
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
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    height: 60px;
    padding: 14px 20px 14px 0;
    text-align: right;
    background: var(--color-bg-2);
    box-shadow: 0 -2px 8px rgb(0 0 0 / 10%);
  }
</style>
