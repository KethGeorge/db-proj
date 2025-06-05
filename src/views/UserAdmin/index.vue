<template>
  <div class="container">
    <Breadcrumb :items="['User', 'User.form']" />
    <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
      <a-space direction="vertical" :size="16">
        <a-card class="general-card" :bordered="false">
          <template #title>
            {{ $t('user.form.title') }}
          </template>
          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item :label="$t('user.form.label.username')" field="username"
                :rules="[{ required: true, message: '用户名不能为空' }]">
                <a-input v-model="formData.username" :placeholder="$t('user.form.placeholder.username')" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item :label="$t('user.form.label.password')" field="password"
                :rules="[{ required: true, message: '密码不能为空' }]">
                <a-input-password v-model="formData.password" :placeholder="$t('user.form.placeholder.password')" />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item :label="$t('user.form.label.email')" field="email"
                :rules="[{ required: true, message: '邮箱不能为空' }, { type: 'email', message: '请输入有效的邮箱地址' }]">
                <a-input v-model="formData.email" :placeholder="$t('user.form.placeholder.email')" />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item :label="$t('user.form.label.telephone')" field="telephone">
                <a-input v-model="formData.telephone" :placeholder="$t('user.form.placeholder.telephone')" />
              </a-form-item>
            </a-col>
          </a-row>

          <a-form-item :label="$t('user.form.label.userPermissions')" field="userPermissions"
            :rules="[{ required: true, message: '用户权限不能为空' }]">
            <a-select v-model="formData.userPermissions" :placeholder="$t('user.form.placeholder.userPermissions')">
              <a-option value="admin">管理员</a-option>
              <a-option value="user">普通用户</a-option>
              <a-option value="guest">访客</a-option>
            </a-select>
          </a-form-item>

          <!-- <a-form-item :label="$t('user.form.label.registrationDate')" field="registrationDate">
            <a-checkbox v-model="formData.registrationDate_disabled" class="date-time-checkbox">
              {{ $t('user.form.label.disableDateTime') }}
            </a-checkbox>
            <a-row :gutter="8" :class="{ 'disabled-row': formData.registrationDate_disabled }">
              <a-col :span="12">
                <a-date-picker v-model="formData.registrationDate_date" style="width: 100%;"
                  :placeholder="$t('user.form.placeholder.registrationDateDate')"
                  :disabled="formData.registrationDate_disabled" />
              </a-col>
              <a-col :span="12">
                <a-time-picker v-model="formData.registrationDate_time" style="width: 100%;" format="HH:mm:ss"
                  :placeholder="$t('user.form.placeholder.registrationDateTime')"
                  :disabled="formData.registrationDate_disabled" />
              </a-col>
            </a-row>
          </a-form-item> -->

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
import axios, { AxiosResponse } from 'axios';
import { useUserStore } from '@/store';

const user = useUserStore();
const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();

// 定义表单数据结构，与后端接收的字段名保持一致
const formData = reactive({
  username: '',
  password: '',
  email: '',
  telephone: '',
  userPermissions: 'user',
//   registrationDate_disabled: false,
//   registrationDate_date: undefined as Date | undefined,
//   registrationDate_time: '' as string,
});

const combineDateTime = (dateObj: Date | undefined, timeStr: string): string | null => {
  if (!dateObj) {
    return null;
  }
  if (!(dateObj instanceof Date)) {
    try {
      const parsedDate = new Date(dateObj);
      if (!Number.isNaN(parsedDate.getTime())) {
        dateObj = parsedDate;
      } else {
        return null;
      }
    } catch (e) {
      return null;
    }
  }

  const year = dateObj.getFullYear();
  const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
  const day = dateObj.getDate().toString().padStart(2, '0');
  const timePart = timeStr || '00:00:00';

  return `${year}-${month}-${day}T${timePart}`;
};

// 假设您的拦截器已经处理了 HttpResponse 结构，
// 这里直接声明 AxiosResponse<any> 因为拦截器会返回 res.data
// 或者如果拦截器返回的是 res 自身（即 HttpResponse），那么可以声明为 AxiosResponse<HttpResponse>
// 但是在 success_response_wrap 中，您返回的是 data，所以这里依然是 AxiosResponse<any> 比较安全
// 因为 success_response_wrap 的 data 是 { username: string; email: string; }
// 因此，这里的 `response` 已经是 `data` 字段的内容了。
// 重要的是，由于拦截器的存在，这里不再需要检查 `response.data.code` 或 `response.data.message`。
// 拦截器在非 20000 情况下已经抛出了错误。
interface HttpResponse<T = any> { // 模拟后端统一返回结构，用于拦截器
  code: number;
  message: string;
  data: T;
}
const resetForm = () => {
  Object.assign(formData, {
    username: '',
    password: '',
    email: '',
    telephone: '',
    userPermissions: 'user',
    registrationDate_disabled: false,
    registrationDate_date: undefined,
    registrationDate_time: '',
  });
  formRef.value?.resetFields();
};


const onSubmitClick = async () => {
  const errors = await formRef.value?.validate();

  if (!errors) {
    setLoading(true);
    try {
    //   let registrationDateValue: string | null = null;
    //   if (!formData.registrationDate_disabled) {
    //     registrationDateValue = combineDateTime(formData.registrationDate_date, formData.registrationDate_time);
    //   }

      const dataToSend: { [key: string]: any } = {
        username: formData.username,
        password: formData.password,
        email: formData.email,
        telephone: formData.telephone,
        userPermissions: formData.userPermissions,
        // registrationDate: registrationDateValue,
        operator: user.userInfo.name || 'unknown_user',
      };

      // 问题2: 由于拦截器存在，这里的 response 已经是后端 success_response_wrap 返回的 data 部分
      // 如果 Flask 的 success_response_wrap 返回的是 { code: 20000, message: "...", data: { ... } }
      // 并且您的拦截器最终返回的是 response.data (即整个 { code, message, data } 对象)
      // 那么这里的 response 应该就是 HttpResponse 结构。
      // 但如果拦截器返回的是 res14ponse.data.data (即 success_response_wrap 中的 data 部分)，
      // 那么这里的 response 就直接是 { username: string; email: string; }。
      // 根据您提供的拦截器代码：`return res;`，这意味着拦截器返回的是完整的 `HttpResponse` 对象。
      // 所以下面的类型声明应该是 `HttpResponse<{ username: string; email: string; }>`
      const response: HttpResponse<{ username: string; email: string; }> = await axios.post('/api/user', dataToSend);

      // 拦截器已经处理了错误，所以如果代码执行到这里，说明请求是成功的 (res.code === 20000)
      // 此时 response 就是 res，即 { code: 20000, message: "...", data: { ... } }
      Message.success(response.message || '用户信息提交成功！'); // 直接访问 response.message
      resetForm();

    } catch (error) {
      // 拦截器会捕获并显示错误信息，这里可以进行其他错误处理，如日志记录或UI反馈
      console.error('提交用户信息失败:', error);
      // 由于拦截器已经处理了 Message.error，这里不再重复显示
      // 可以根据需要添加其他 UI 提示
    } finally {
      setLoading(false);
    }
  } else {
    Message.warning('请检查并填写所有必填项！');
  }
};

</script>

<script lang="ts">
export default {
  name: 'UserForm',
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