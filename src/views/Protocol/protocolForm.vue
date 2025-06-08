<template>
  <div class="container">
    <Breadcrumb
      :items="[
        'protocol',
        isCreate
          ? 'protocol.form.title.create'
          : isEdit
          ? 'protocol.form.title.edit'
          : 'protocol.form.title.view',
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
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.ProtocolNo')"
                field="ProtocolNo"
                :rules="[
                  {
                    required: true,
                    message: $t('protocol.form.validation.ProtocolNoRequired'),
                  },
                  {
                    min: 1,
                    max: 8,
                    message: $t('protocol.form.validation.ProtocolNoLength'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.ProtocolNo"
                  :placeholder="$t('protocol.form.placeholder.ProtocolNo')"
                  :disabled="!isCreate"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.MaterialCode')"
                field="MaterialCode"
                :rules="[
                  {
                    required: true,
                    message: $t(
                      'protocol.form.validation.MaterialCodeRequired'
                    ),
                  },
                  {
                    min: 1,
                    max: 16,
                    message: $t('protocol.form.validation.MaterialCodeLength'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.MaterialCode"
                  :placeholder="$t('protocol.form.placeholder.MaterialCode')"
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.UserNo')"
                field="UserNo"
                :rules="[
                  {
                    required: true,
                    message: $t('protocol.form.validation.UserNoRequired'),
                  },
                  {
                    min: 1,
                    max: 8,
                    message: $t('protocol.form.validation.UserNoLength'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.UserNo"
                  :placeholder="$t('protocol.form.placeholder.UserNo')"
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.NSN')"
                field="NSN"
                :rules="[
                  {
                    max: 20,
                    message: $t('protocol.form.validation.NSNLength'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.NSN"
                  :placeholder="$t('protocol.form.placeholder.NSN')"
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.SHT')"
                field="SHT"
                :rules="[
                  {
                    type: 'number',
                    message: $t('protocol.form.validation.SHTNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="shtComputed"
                  :placeholder="$t('protocol.form.placeholder.SHT')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.1"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.SMS')"
                field="SMS"
                :rules="[
                  {
                    type: 'number',
                    message: $t('protocol.form.validation.SMSNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="smsComputed"
                  :placeholder="$t('protocol.form.placeholder.SMS')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.1"
                  allow-clear
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.MixingAngle')"
                field="MixingAngle"
                :rules="[
                  {
                    type: 'number',
                    message: $t('protocol.form.validation.MixingAngleNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="mixingAngleComputed"
                  :placeholder="$t('protocol.form.placeholder.MixingAngle')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.1"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.MixingRadius')"
                field="MixingRadius"
                :rules="[
                  {
                    type: 'number',
                    message: $t('protocol.form.validation.MixingRadiusNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="mixingRadiusComputed"
                  :placeholder="$t('protocol.form.placeholder.MixingRadius')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.1"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('protocol.form.label.MeasurementInterval')"
                field="MeasurementInterval"
                :rules="[
                  {
                    type: 'number',
                    message: $t(
                      'protocol.form.validation.MeasurementIntervalNumber'
                    ),
                  },
                ]"
              >
                <a-input-number
                  v-model="measurementIntervalComputed"
                  :placeholder="
                    $t('protocol.form.placeholder.MeasurementInterval')
                  "
                  :disabled="!isEdit && !isCreate"
                  :step="0.1"
                  allow-clear
                />
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
  import {
    queryProtocolDetail,
    createProtocol,
    updateProtocolInfo,
    ProtocolRecord,
  } from '@/api/protocol';
  import { useRoute, useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import cloneDeep from 'lodash/cloneDeep';

  const formRef = ref<FormInstance>();
  const { loading, setLoading } = useLoading();
  const route = useRoute();
  const router = useRouter();
  const { t } = useI18n();

  const formData = reactive<ProtocolRecord>({
    ProtocolNo: '',
    NSN: undefined,
    SHT: undefined, // 初始化为 undefined
    SMS: undefined,
    MixingAngle: undefined,
    MixingRadius: undefined,
    MeasurementInterval: undefined,
    MaterialCode: '',
    UserNo: '',
  });

  const protocolNoFromRoute = computed(
    () => route.params.protocolNo as string | undefined
  );
  const isCreate = computed(() => route.name === 'ProtocolAdminCreate');
  const isEdit = computed(() => route.name === 'ProtocolAdminEdit');
  const isView = computed(() => route.name === 'ProtocolAdminView');

  const formTitle = computed(() => {
    if (isCreate.value) return 'protocol.form.title.create';
    if (isEdit.value) return 'protocol.form.title.edit';
    if (isView.value) return 'protocol.form.title.view';
    return 'protocol.form.title.default';
  });

  // 计算属性，用于 a-input-number 的双向绑定，处理 null/undefined 转换
  const createNumberComputed = (key: keyof ProtocolRecord) =>
    computed({
      get: () => {
        const value = formData[key];
        return value === null ? undefined : (value as number | undefined); // 确保类型为 number | undefined
      },
      set: (value: number | undefined) => {
        // 组件会传 undefined 当清空时，我们希望存为 null
        (formData[key] as number | null | undefined) =
          value === undefined ? null : value;
      },
    });

  const shtComputed = createNumberComputed('SHT');
  const smsComputed = createNumberComputed('SMS');
  const mixingAngleComputed = createNumberComputed('MixingAngle');
  const mixingRadiusComputed = createNumberComputed('MixingRadius');
  const measurementIntervalComputed = createNumberComputed(
    'MeasurementInterval'
  );

  // 获取协议详情数据
  const fetchProtocolData = async (protocolNo: string) => {
    setLoading(true);
    try {
      const res = await queryProtocolDetail(protocolNo);
      Object.assign(formData, res);
    } catch (error: any) {
      Message.error(
        `${t('protocol.message.fetchFail')}: ${error.message || '未知错误'}`
      );
      console.error('Error fetching protocol data:', error);
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    if (isCreate.value) {
      Object.assign(formData, {
        ProtocolNo: '',
        NSN: undefined,
        SHT: undefined,
        SMS: undefined,
        MixingAngle: undefined,
        MixingRadius: undefined,
        MeasurementInterval: undefined,
        MaterialCode: '',
        UserNo: '',
      });
      formRef.value?.resetFields();
    } else if (protocolNoFromRoute.value) {
      fetchProtocolData(protocolNoFromRoute.value);
    }
  };

  watch(
    () => route.params.protocolNo,
    (newVal) => {
      if ((isEdit.value || isView.value) && newVal) {
        fetchProtocolData(newVal as string);
      } else if (isCreate.value) {
        resetForm();
      }
    },
    { immediate: true }
  );

  onMounted(() => {
    if ((isEdit.value || isView.value) && protocolNoFromRoute.value) {
      fetchProtocolData(protocolNoFromRoute.value);
    }
  });

  const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
      setLoading(true);
      try {
        const dataToSend: Partial<ProtocolRecord> = cloneDeep(formData);

        // 统一处理可能为空的字段：将 undefined 或 '' 转换为 null
        const nullableStringFields: (keyof ProtocolRecord)[] = ['NSN'];
        nullableStringFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        // 浮点数类型字段，处理 undefined 或 '' 转换为 null (这个在 computed setter 已经做了，但这里是最终发送前的确认)
        const nullableNumberFields: (keyof ProtocolRecord)[] = [
          'SHT',
          'SMS',
          'MixingAngle',
          'MixingRadius',
          'MeasurementInterval',
        ];
        nullableNumberFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        if (isCreate.value) {
          await createProtocol(dataToSend as ProtocolRecord);
          Message.success(t('protocol.message.createSuccess'));
          router.push({ name: 'ProtocolAdminList' });
        } else if (isEdit.value) {
          if (!protocolNoFromRoute.value) {
            Message.error(t('protocol.message.idMissingForUpdate'));
            setLoading(false);
            return;
          }
          await updateProtocolInfo(protocolNoFromRoute.value, dataToSend);
          Message.success(t('protocol.message.updateSuccess'));
          router.push({ name: 'ProtocolAdminList' });
        }
      } catch (error: any) {
        console.error('提交协议信息失败:', error);
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
    name: 'ProtocolForm',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 40px;
    overflow: hidden;
  }

  :deep(.arco-select-view-disabled),
  :deep(.arco-input-disabled),
  :deep(.arco-textarea-disabled),
  :deep(.arco-input-number-disabled) {
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
