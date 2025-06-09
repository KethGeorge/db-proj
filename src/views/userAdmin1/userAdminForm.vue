<template>
  <div class="container">
    <Breadcrumb
      :items="[
        'User',
        isCreate
          ? 'userAdmin.form.title.create'
          : isEdit
          ? 'userAdmin.form.title.edit'
          : 'userAdmin.form.title.view',
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
                :label="$t('userAdmin.form.label.UserNo')"
                field="UserNo"
                :rules="[
                  { message: $t('userAdmin.form.validation.UserNoRequired') },
                  {
                    min: 8,
                    max: 8,
                    message: $t('userAdmin.form.validation.UserNoLength'),
                  },
                ]"
              >
                <a-input
                  v-model="formData.UserNo"
                  :placeholder="$t('userAdmin.form.placeholder.UserNo')"
                  :disabled="!isCreate"
                />
                <!-- UserNo 仅在创建时可编辑 -->
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('userAdmin.form.label.UserName')"
                field="UserName"
                :rules="[
                  {
                    required: true,
                    message: $t('userAdmin.form.validation.UserNameRequired'),
                  },
                  {
                    min: 1,
                    max: 20,
                    message: $t('userAdmin.form.validation.UserNameLength'),
                  },
                ]"
              >
                <a-input
                  v-model="userNameComputed"
                  :placeholder="$t('userAdmin.form.placeholder.UserName')"
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                v-if="isCreate"
                :label="$t('userAdmin.form.label.UserPassword')"
                field="UserPassword"
                :rules="[
                  {
                    required: true,
                    message: $t(
                      'userAdmin.form.validation.UserPasswordRequired'
                    ),
                  },
                  {
                    min: 6,
                    message: $t('userAdmin.form.validation.UserPasswordLength'),
                  },
                  {
                    max: 20,
                    message: $t(
                      'userAdmin.form.validation.UserPasswordMaxLength'
                    ),
                  },
                ]"
              >
                <a-input-password
                  v-model="userPasswordComputed"
                  :placeholder="$t('userAdmin.form.placeholder.UserPassword')"
                />
              </a-form-item>
              <a-form-item
                v-else-if="isEdit"
                :label="$t('userAdmin.form.label.NewUserPassword')"
                field="UserPassword"
                :rules="[
                  {
                    min: 6,
                    message: $t('userAdmin.form.validation.UserPasswordLength'),
                  },
                  {
                    max: 20,
                    message: $t(
                      'userAdmin.form.validation.UserPasswordMaxLength'
                    ),
                  },
                ]"
              >
                <a-input-password
                  v-model="userPasswordComputed"
                  :placeholder="
                    $t('userAdmin.form.placeholder.NewUserPassword')
                  "
                />
              </a-form-item>
              <a-form-item
                v-else
                :label="$t('userAdmin.form.label.UserPassword')"
              >
                <a-input value="********" disabled />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('userAdmin.form.label.Email')"
                field="Email"
                :rules="[
                  {
                    type: 'email',
                    message: $t('userAdmin.form.validation.EmailInvalid'),
                  },
                  {
                    max: 20,
                    message: $t('userAdmin.form.validation.EmailLength'),
                  },
                ]"
              >
                <a-input
                  v-model="userEmailComputed"
                  :placeholder="$t('userAdmin.form.placeholder.Email')"
                  :disabled="!isEdit && !isCreate"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                :label="$t('userAdmin.form.label.UserPermissions')"
                field="UserPermissions"
                :rules="[
                  {
                    max: 5,
                    message: $t(
                      'userAdmin.form.validation.UserPermissionsLength'
                    ),
                  },
                ]"
              >
                <a-select
                  v-model="userPermissionsComputed"
                  :placeholder="
                    $t('userAdmin.form.placeholder.UserPermissions')
                  "
                  :disabled="!isEdit && !isCreate"
                  :allow-clear="true"
                >
                  <a-option value="admin">{{
                    $t('userAdmin.form.UserPermissions.admin')
                  }}</a-option>
                  <a-option value="user">{{
                    $t('userAdmin.form.UserPermissions.user')
                  }}</a-option>
                  <a-option value="guest">{{
                    $t('userAdmin.form.UserPermissions.guest')
                  }}</a-option>
                </a-select>
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('userAdmin.form.label.Telephone')"
                field="Telephone"
                :rules="[
                  {
                    max: 13,
                    message: $t('userAdmin.form.validation.TelephoneLength'),
                  },
                ]"
              >
                <a-input
                  v-model="userTelephoneComputed"
                  :placeholder="$t('userAdmin.form.placeholder.Telephone')"
                  :disabled="!isEdit && !isCreate"
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
    queryUserDetail,
    createUser,
    updateUserInfo,
    type UserRecord,
  } from '@/api/userAdmin'; // <-- 导入新 API
  import { useRoute, useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import cloneDeep from 'lodash/cloneDeep';

  const formRef = ref<FormInstance>();
  const { loading, setLoading } = useLoading();
  const route = useRoute();
  const router = useRouter();
  const { t } = useI18n();

  // formData 现在直接匹配 UserRecord 接口，但 UserPassword 在编辑时将是空的
  const formData = reactive<UserRecord>({
    UserNo: '', // UserNo 在创建时可能由后端生成，但前端输入框默认为空字符串
    UserName: '',
    UserPassword: '', // 创建时必填
    UserPermissions: undefined, // 可选
    Email: undefined, // 可选
    Telephone: undefined, // 可选
  });

  const usernoFromRoute = computed(
    () => route.params.userno as string | undefined
  );
  const isCreate = computed(() => route.name === 'UserAdminCreate');
  const isEdit = computed(() => route.name === 'UserAdminEdit');
  const isView = computed(() => route.name === 'UserAdminView');

  const formTitle = computed(() => {
    if (isCreate.value) return 'userAdmin.form.title.create';
    if (isEdit.value) return 'userAdmin.form.title.edit';
    if (isView.value) return 'userAdmin.form.title.view';
    return 'userAdmin.form.title.default';
  });

  // 计算属性工厂，处理 string | null | undefined 类型 (用于 a-input 和 a-select)
  const createNullableStringComputed = <
    K extends
      | 'UserName'
      | 'UserPassword'
      | 'UserPermissions'
      | 'Email'
      | 'Telephone'
  >(
    key: K
  ) =>
    computed({
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

  const userNameComputed = createNullableStringComputed('UserName');
  const userPasswordComputed = createNullableStringComputed('UserPassword');
  const userPermissionsComputed =
    createNullableStringComputed('UserPermissions');
  const userEmailComputed = createNullableStringComputed('Email');
  const userTelephoneComputed = createNullableStringComputed('Telephone');

  // 获取用户详情数据
  const fetchUserData = async (userno: string) => {
    setLoading(true);
    try {
      const res = await queryUserDetail(userno);
      // 填充表单数据，注意这里后端返回的 UserPassword 已经被 '********' 屏蔽
      Object.assign(formData, res);
      formData.UserPassword = ''; // 密码字段不回填实际值
    } catch (error: any) {
      Message.error(
        `${t('userAdmin.message.fetchFail')}: ${error.message || '未知错误'}`
      );
      console.error('Error fetching user data:', error);
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    if (isCreate.value) {
      Object.assign(formData, {
        UserNo: '', // 创建模式，UserNo 允许用户输入或留空生成
        UserName: '',
        UserPassword: '',
        UserPermissions: undefined,
        Email: undefined,
        Telephone: undefined,
      });
      formRef.value?.resetFields();
    } else {
      formData.UserPassword = ''; // 编辑模式只清空密码，其他数据重新加载
      if (usernoFromRoute.value) {
        fetchUserData(usernoFromRoute.value);
      }
    }
  };

  watch(
    () => route.params.userno,
    (newVal) => {
      if ((isEdit.value || isView.value) && newVal) {
        fetchUserData(newVal as string);
      } else if (isCreate.value) {
        resetForm();
      }
    },
    { immediate: true }
  );

  onMounted(() => {
    if ((isEdit.value || isView.value) && usernoFromRoute.value) {
      fetchUserData(usernoFromRoute.value);
    } else if (isCreate.value) {
      resetForm();
    }
  });

  const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
      setLoading(true);
      try {
        const dataToSend: Partial<UserRecord> = cloneDeep(formData);

        // 统一处理可能为空的字符串字段：将 undefined 或 '' 转换为 null
        const nullableStringFields: (keyof UserRecord)[] = [
          'UserPermissions',
          'Email',
          'Telephone',
        ];
        nullableStringFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        // 密码字段处理
        if (
          !isCreate.value &&
          (!dataToSend.UserPassword || dataToSend.UserPassword.trim() === '')
        ) {
          // 如果是编辑模式，且没有输入新密码或输入为空白，则不发送密码字段
          delete dataToSend.UserPassword;
        }

        let response;
        if (isCreate.value) {
          // UserNo 在创建时可能由后端生成，或由前端提供
          if (!dataToSend.UserNo || dataToSend.UserNo.trim() === '') {
            // 如果前端没有提供或为空白，就删除该字段，让后端生成
            delete dataToSend.UserNo;
          }
          response = await createUser(dataToSend as UserRecord); // 必填校验在前端，这里直接断言
          if (response && response.UserNo) {
            // 假设后端返回了生成的UserNo
            Message.success(
              `${t('userAdmin.message.createSuccess')}: ${response.UserNo}`
            );
          } else {
            Message.success(t('userAdmin.message.createSuccess'));
          }
        } else if (isEdit.value) {
          if (!usernoFromRoute.value) {
            Message.error(t('userAdmin.message.idMissingForUpdate'));
            setLoading(false);
            return;
          }
          // UserNo 不应在更新时修改，确保请求体中不包含 UserNo (已包含在路由参数中)
          delete dataToSend.UserNo;
          response = await updateUserInfo(usernoFromRoute.value, dataToSend);
          Message.success(t('userAdmin.message.updateSuccess'));
        } else {
          return;
        }
        router.push({ name: 'UserAdminList' }); // 提交成功后返回列表页
      } catch (error: any) {
        console.error('提交用户信息失败:', error);
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
    name: 'UserForm',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 40px;
  }

  :deep(.arco-select-view-disabled),
  :deep(.arco-input-disabled),
  :deep(.arco-textarea-disabled),
  :deep(.arco-input-password-disabled) {
    /* 添加 input-password 的 disabled 样式 */
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
