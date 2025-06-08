<template>
  <div class="container">
    <Breadcrumb
      :items="[
        'experiment',
        isCreate
          ? 'experiment.form.title.create'
          : isEdit
          ? 'experiment.form.title.edit'
          : 'experiment.form.title.view',
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
                :label="$t('experiment.form.label.ExperimentNo')"
                field="ExperimentNo"
                :rules="[
                  {
                    required: true,
                    message: $t(
                      'experiment.form.validation.ExperimentNoRequired'
                    ),
                  },
                  {
                    min: 1,
                    max: 16,
                    message: $t(
                      'experiment.form.validation.ExperimentNoLength'
                    ),
                  },
                ]"
              >
                <a-input
                  v-model="formData.ExperimentNo"
                  :placeholder="$t('experiment.form.placeholder.ExperimentNo')"
                  :disabled="!isCreate"
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.MaterialCode')"
                field="MaterialCode"
                :rules="[
                  {
                    max: 16,
                    message: $t(
                      'experiment.form.validation.MaterialCodeLength'
                    ),
                  },
                ]"
              >
                <a-select
                  v-model="materialCodeComputed"
                  :placeholder="$t('experiment.form.placeholder.MaterialCode')"
                  :disabled="!isEdit && !isCreate"
                  :allow-clear="true"
                  :show-search="true"
                  :filter-option="false"
                  :allow-search="true"
                  @change="handleMaterialChange"
                  @search="handleMaterialSearch"
                >
                  <a-option
                    v-for="item in materialOptions"
                    :key="item.MaterialCode"
                    :value="item.MaterialCode"
                  >
                    {{ item.MaterialName }} ({{ item.MaterialCode }})
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.ProtocolNo')"
                field="ProtocolNo"
                :rules="[
                  {
                    max: 8,
                    message: $t('experiment.form.validation.ProtocolNoLength'),
                  },
                ]"
              >
                <a-select
                  v-model="protocolNoComputed"
                  :placeholder="$t('experiment.form.placeholder.ProtocolNo')"
                  :disabled="!isEdit && !isCreate"
                  :allow-clear="true"
                  :show-search="true"
                  :filter-option="false"
                  :allow-search="true"
                  @search="handleProtocolSearch"
                  @change="handleProtocolChange"
                >
                  <a-option
                    v-for="item in protocolOptions"
                    :key="item.ProtocolNo"
                    :value="item.ProtocolNo"
                  >
                    {{ item.ProtocolNo }} ({{
                      item.NSN || $t('groupForm.noDescription')
                    }})
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.UserNo')"
                field="UserNo"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.UserNoRequired'),
                  },
                  {
                    min: 1,
                    max: 8,
                    message: $t('experiment.form.validation.UserNoLength'),
                  },
                ]"
              >
                <a-select
                  v-model="formData.UserNo"
                  :placeholder="$t('experiment.form.placeholder.UserNo')"
                  :disabled="!isEdit && !isCreate"
                  :allow-clear="true"
                  :show-search="true"
                  :filter-option="false"
                  :allow-search="true"
                  @search="handleUserSearch"
                  @change="handleUserChange"
                >
                  <a-option
                    v-for="item in userOptions"
                    :key="item.UserNo"
                    :value="item.UserNo"
                  >
                    {{ item.UserName }} ({{ item.UserNo }})
                  </a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.HeatError')"
                field="HeatError"
                :rules="[
                  {
                    type: 'number',
                    message: $t('experiment.form.validation.HeatErrorNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="heatErrorComputed"
                  :placeholder="$t('experiment.form.placeholder.HeatError')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.01"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.MixError')"
                field="MixError"
                :rules="[
                  {
                    type: 'number',
                    message: $t('experiment.form.validation.MixErrorNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="mixErrorComputed"
                  :placeholder="$t('experiment.form.placeholder.MixError')"
                  :disabled="!isEdit && !isCreate"
                  :step="0.01"
                  allow-clear
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.StartTime')"
                field="StartTime"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.StartTimeRequired'),
                  },
                ]"
              >
                <a-time-picker
                  v-model="startTimeComputed"
                  :placeholder="$t('experiment.form.placeholder.StartTime')"
                  :disabled="!isEdit && !isCreate"
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <a-form-item
                :label="$t('experiment.form.label.EndTime')"
                field="EndTime"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.EndTimeRequired'),
                  },
                ]"
              >
                <a-time-picker
                  v-model="endTimeComputed"
                  :placeholder="$t('experiment.form.placeholder.EndTime')"
                  :disabled="!isEdit && !isCreate"
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                  allow-clear
                />
              </a-form-item>
            </a-col>
            <a-col :span="8">
              <!-- DeviceNo 字段已移除 -->
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
  import { FormInstance } from '@arco-design/web-vue'; // 修正导入路径
  import { Message } from '@arco-design/web-vue';
  import useLoading from '@/hooks/loading';
  import {
    queryExperimentDetail,
    createExperiment,
    updateExperimentInfo,
    type ExperimentRecord,
  } from '@/api/experiment';
  import { searchMaterials, type MaterialRecord } from '@/api/materials';
  import { searchProtocols, type ProtocolSearchRecord } from '@/api/protocol';
  import { searchUsers, type UserSearchRecord } from '@/api/userAdmin';
  // 移除 Device 搜索 API 和类型
  // import { searchDevices, type DeviceSearchRecord } from '@/api/device';

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
    // DeviceNo 字段已移除
    // DeviceNo: undefined,
  });

  const experimentNoFromRoute = computed(
    () => route.params.experimentNo as string | undefined
  );
  const isCreate = computed(() => route.name === 'ExperimentAdminCreate');
  const isEdit = computed(() => route.name === 'ExperimentAdminEdit');
  const isView = computed(() => route.name === 'ExperimentAdminView');

  const formTitle = computed(() => {
    if (isCreate.value) return 'experiment.form.title.create';
    if (isEdit.value) return 'experiment.form.title.edit';
    if (isView.value) return 'experiment.form.title.view';
    return 'experiment.form.title.default';
  });

  // 计算属性工厂，处理 number | null | undefined 类型 (用于 a-input-number)
  const createNumberComputed = (key: 'HeatError' | 'MixError') =>
    computed({
      get: () => {
        const value = formData[key];
        return value === null ? undefined : (value as number | undefined);
      },
      set: (value: number | undefined) => {
        (formData[key] as number | null | undefined) =
          value === undefined ? null : value;
      },
    });

  const heatErrorComputed = createNumberComputed('HeatError');
  const mixErrorComputed = createNumberComputed('MixError');

  // 计算属性工厂，处理 string | null | undefined 类型 (用于 a-select 的 MaterialCode, ProtocolNo)
  const createNullableStringComputed = <
    K extends 'MaterialCode' | 'ProtocolNo'
  >(
    key: K
  ) =>
    computed({
      // 修正 K 类型，移除 DeviceNo
      get: () => {
        const value = formData[key];
        return value === null || value === ''
          ? undefined
          : (value as string | undefined);
      },
      set: (value: string | undefined) => {
        (formData[key] as string | null | undefined) =
          value === undefined || value === '' ? null : value;
      },
    });

  const materialCodeComputed = createNullableStringComputed('MaterialCode');
  const protocolNoComputed = createNullableStringComputed('ProtocolNo');

  // ExperimentNo 是必填字符串，UserNo 是必填字符串，直接绑定 formData.ExperimentNo 和 formData.UserNo。

  // 计算属性工厂，用于 a-time-picker 的双向绑定，处理 null/undefined/'' 转换
  const createTimeComputed = (key: 'StartTime' | 'EndTime') =>
    computed({
      get: () => {
        const value = formData[key];
        return value === null ? undefined : (value as string | undefined);
      },
      set: (value: string | undefined) => {
        formData[key] = value === undefined || value === '' ? null : value;
      },
    });

  const startTimeComputed = createTimeComputed('StartTime');
  const endTimeComputed = createTimeComputed('EndTime');

  // --- 外键选择器相关逻辑 START ---
  // 材料选择器相关
  const materialOptions = ref<MaterialRecord[]>([]);
  const materialSearchTimeout = ref<number | null>(null);
  // 移除 materialSearchValue，因为不再手动管理 input-value
  // const materialSearchValue = ref<string>('');

  const handleMaterialSearch = async (searchValue: string) => {
    console.log('MaterialSearch triggered with:', searchValue);
    if (materialSearchTimeout.value) {
      clearTimeout(materialSearchTimeout.value);
    }
    materialOptions.value = []; // 每次搜索前清空旧选项，避免显示不相关的旧选项
    if (!searchValue) {
      return;
    }
    // 防抖处理：等待 300ms 后再发送请求
    materialSearchTimeout.value = setTimeout(async () => {
      try {
        const result = await searchMaterials({ query: searchValue });
        materialOptions.value = result;
        console.log('Material search results:', result);
      } catch (error) {
        console.error('搜索材料失败:', error);
        Message.error('搜索材料失败');
        materialOptions.value = [];
      }
    }, 300) as unknown as number;
  };

  // 修正 handleMaterialChange 的参数类型，使其能接受 Arco Design Vue 的 a-select @change 事件的实际复杂类型
  const handleMaterialChange = (
    value:
      | string
      | number
      | Record<string, any>
      | undefined
      | (string | number | Record<string, any>)[]
      | boolean
  ) => {
    if (Array.isArray(value) || typeof value === 'boolean') {
      // 对于多选数组或布尔值，视为清空或无效操作
      materialOptions.value = [];
      return;
    }
    // value 就是 materialCodeComputed setter 接收到的值
    // 这里不需要额外设置 materialSearchValue，因为 a-select 会根据 v-model 自动显示其 label
    // 并且我们移除了 input-value 绑定
    materialCodeComputed.value = value as string | undefined; // 明确赋值给计算属性，触发其setter
  };

  // 移除 handleMaterialInputValueChange，因为不再手动管理 input-value
  // const handleMaterialInputValueChange = (value: string) => { /* ... */ };

  // 协议选择器相关
  const protocolOptions = ref<ProtocolSearchRecord[]>([]);
  const protocolSearchTimeout = ref<number | null>(null);
  // 移除 protocolSearchValue
  // const protocolSearchValue = ref<string>('');

  const handleProtocolSearch = async (searchValue: string) => {
    console.log('ProtocolSearch triggered with:', searchValue);
    if (protocolSearchTimeout.value) {
      clearTimeout(protocolSearchTimeout.value);
    }
    protocolOptions.value = [];
    if (!searchValue) {
      return;
    }
    protocolSearchTimeout.value = setTimeout(async () => {
      try {
        const result = await searchProtocols({ query: searchValue });
        protocolOptions.value = result;
        console.log('Protocol search results:', result);
      } catch (error) {
        console.error('搜索协议失败:', error);
        Message.error('搜索协议失败');
        protocolOptions.value = [];
      }
    }, 300) as unknown as number;
  };

  const handleProtocolChange = (
    value:
      | string
      | number
      | Record<string, any>
      | undefined
      | (string | number | Record<string, any>)[]
      | boolean
  ) => {
    if (Array.isArray(value) || typeof value === 'boolean') {
      protocolOptions.value = [];
      return;
    }
    // 移除对 protocolSearchValue 的操作
    protocolNoComputed.value = value as string | undefined; // 确保 v-model 绑定的计算属性被更新
  };

  // 移除 handleProtocolInputValueChange
  // const handleProtocolInputValueChange = (value: string) => { /* ... */ };

  // 用户选择器相关
  const userOptions = ref<UserSearchRecord[]>([]);
  const userSearchTimeout = ref<number | null>(null);
  // 移除 userSearchValue
  // const userSearchValue = ref<string>('');

  const handleUserSearch = async (searchValue: string) => {
    console.log('UserSearch triggered with:', searchValue);
    if (userSearchTimeout.value) {
      clearTimeout(userSearchTimeout.value);
    }
    userOptions.value = [];
    if (!searchValue) {
      return;
    }
    userSearchTimeout.value = setTimeout(async () => {
      try {
        const result = await searchUsers({ query: searchValue });
        userOptions.value = result;
        console.log('User search results:', result);
      } catch (error) {
        console.error('搜索用户失败:', error);
        Message.error('搜索用户失败');
        userOptions.value = [];
      }
    }, 300) as unknown as number;
  };

  const handleUserChange = (
    value:
      | string
      | number
      | Record<string, any>
      | undefined
      | (string | number | Record<string, any>)[]
      | boolean
  ) => {
    if (Array.isArray(value) || typeof value === 'boolean') {
      userOptions.value = [];
      return;
    }
    if (value === undefined || value === null || value === '') {
      formData.UserNo = ''; // UserNo 是必填，如果清空，确保 formData.UserNo 变为 ''
    } else {
      // v-model 已经绑定到 formData.UserNo，这里不需要再赋值
      // formData.UserNo = value as string; // 这行应该由 v-model 自动处理
      formData.UserNo = value.toString(); // 确保是 string，如果 v-model 没起作用
    }
    // 移除对 userSearchValue 的操作
  };

  // 移除 handleUserInputValueChange
  // const handleUserInputValueChange = (value: string) => { /* ... */ };

  // 移除 DeviceNo 相关的计算属性和处理函数
  /*
const deviceOptions = ref<DeviceSearchRecord[]>([]);
const deviceSearchTimeout = ref<number | null>(null);
const deviceSearchValue = ref<string>('');

const handleDeviceSearch = async (searchValue: string) => { /* ... * / };
const handleDeviceChange = (value: string | number | Record<string, any> | undefined | (string | number | Record<string, any>)[] | boolean) => { /* ... * / };
const handleDeviceInputValueChange = (value: string) => { /* ... * / };
*/
  // --- 外键选择器相关逻辑 END ---

  // 获取实验详情数据
  const fetchExperimentData = async (experimentNo: string) => {
    setLoading(true);
    try {
      const res = await queryExperimentDetail(experimentNo);
      Object.assign(formData, res);

      // --- 编辑/查看模式下，加载外键对应的显示名称 START ---
      // MaterialCode
      if (formData.MaterialCode) {
        console.log('Fetching initial Material for:', formData.MaterialCode);
        try {
          const currentMaterial = await searchMaterials({
            query: formData.MaterialCode,
          });
          if (
            currentMaterial.length > 0 &&
            currentMaterial[0].MaterialCode === formData.MaterialCode
          ) {
            if (
              !materialOptions.value.some(
                (item) => item.MaterialCode === currentMaterial[0].MaterialCode
              )
            ) {
              materialOptions.value.push(currentMaterial[0]);
            }
            // 移除 materialSearchValue 的设置，因为不再手动管理 input-value
            // materialSearchValue.value = `${currentMaterial[0].MaterialName} (${currentMaterial[0].MaterialCode})`;
          } else {
            console.log(
              'Initial Material not found or mismatched for:',
              formData.MaterialCode
            );
            formData.MaterialCode = undefined;
            // 移除 materialSearchValue 的设置
            // materialSearchValue.value = '';
          }
        } catch (e) {
          console.error('加载已选材料信息失败:', e);
          formData.MaterialCode = undefined;
          // 移除 materialSearchValue 的设置
          // materialSearchValue.value = '';
        }
      }
      // ProtocolNo
      if (formData.ProtocolNo) {
        console.log('Fetching initial Protocol for:', formData.ProtocolNo);
        try {
          const currentProtocol = await searchProtocols({
            query: formData.ProtocolNo,
          });
          if (
            currentProtocol.length > 0 &&
            currentProtocol[0].ProtocolNo === formData.ProtocolNo
          ) {
            if (
              !protocolOptions.value.some(
                (item) => item.ProtocolNo === currentProtocol[0].ProtocolNo
              )
            ) {
              protocolOptions.value.push(currentProtocol[0]);
            }
            // 移除 protocolSearchValue 的设置
            // protocolSearchValue.value = `${currentProtocol[0].ProtocolNo} (${currentProtocol[0].NSN || '无描述'})`;
          } else {
            console.log(
              'Initial Protocol not found or mismatched for:',
              formData.ProtocolNo
            );
            formData.ProtocolNo = undefined;
            // 移除 protocolSearchValue 的设置
            // protocolSearchValue.value = '';
          }
        } catch (e) {
          console.error('加载已选协议信息失败:', e);
          formData.ProtocolNo = undefined;
          // 移除 protocolSearchValue 的设置
          // protocolSearchValue.value = '';
        }
      }
      // UserNo
      if (formData.UserNo) {
        console.log('Fetching initial User for:', formData.UserNo);
        try {
          const currentUser = await searchUsers({ query: formData.UserNo });
          if (
            currentUser.length > 0 &&
            currentUser[0].UserNo === formData.UserNo
          ) {
            if (
              !userOptions.value.some(
                (item) => item.UserNo === currentUser[0].UserNo
              )
            ) {
              userOptions.value.push(currentUser[0]);
            }
            // 移除 userSearchValue 的设置
            // userSearchValue.value = `${currentUser[0].UserName} (${currentUser[0].UserNo})`;
          } else {
            console.log(
              'Initial User not found or mismatched for:',
              formData.UserNo
            );
            formData.UserNo = '';
            // 移除 userSearchValue 的设置
            // userSearchValue.value = '';
          }
        } catch (e) {
          console.error('加载已选用户信息失败:', e);
          formData.UserNo = '';
          // 移除 userSearchValue 的设置
          // userSearchValue.value = '';
        }
      }
      // DeviceNo (因为需求中已移除，所以这里的逻辑也移除)
      /*
        if (formData.DeviceNo) {
            console.log("Fetching initial Device for:", formData.DeviceNo);
            try {
                const currentDevice = await searchDevices({ query: formData.DeviceNo });
                if (currentDevice.length > 0 && currentDevice[0].DeviceNo === formData.DeviceNo) {
                    if (!deviceOptions.value.some(item => item.DeviceNo === currentDevice[0].DeviceNo)) {
                        deviceOptions.value.push(currentDevice[0]);
                    }
                } else {
                    console.log("Initial Device not found or mismatched for:", formData.DeviceNo);
                    formData.DeviceNo = undefined;
                }
            } catch (e) {
                console.error('加载已选设备信息失败:', e);
                formData.DeviceNo = undefined;
            }
        }
        */
      // --- 编辑/查看模式下，加载外键对应的显示名称 END ---
    } catch (error: any) {
      Message.error(
        `${t('experiment.message.fetchFail')}: ${error.message || '未知错误'}`
      );
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
      // DeviceNo 字段已移除
      // DeviceNo: undefined,
    });
    formRef.value?.resetFields();
    // 重置搜索结果选项
    materialOptions.value = [];
    // 移除 materialSearchValue 的重置
    // materialSearchValue.value = '';
    protocolOptions.value = [];
    // 移除 protocolSearchValue 的重置
    // protocolSearchValue.value = '';
    userOptions.value = [];
    // 移除 userSearchValue 的重置
    // userSearchValue.value = '';
    // 移除 DeviceOptions 的重置
    // deviceOptions.value = [];
    // 移除 DeviceSearchValue 的重置
    // deviceSearchValue.value = '';
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
    } else if (isCreate.value) {
      resetForm();
    }
  });

  const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
      setLoading(true);
      try {
        const dataToSend: Partial<ExperimentRecord> = cloneDeep(formData);

        // 移除 DeviceNo 相关的处理
        const nullableStringFields: (keyof ExperimentRecord)[] = [
          'MaterialCode',
          'ProtocolNo',
        ]; // 修正 K 类型，移除 DeviceNo
        nullableStringFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        const nullableNumberFields: (keyof ExperimentRecord)[] = [
          'HeatError',
          'MixError',
        ];
        nullableNumberFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        const nullableTimeFields: (keyof ExperimentRecord)[] = [
          'StartTime',
          'EndTime',
        ];
        nullableTimeFields.forEach((key) => {
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
    name: 'ExperimentForm',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 40px;
  }

  :deep(.arco-select-view-disabled),
  :deep(.arco-input-disabled),
  :deep(.arco-textarea-disabled),
  :deep(.arco-input-number-disabled),
  :deep(.arco-picker-disabled) {
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
  }</style
>/style>
