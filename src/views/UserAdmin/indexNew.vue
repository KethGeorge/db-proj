<template>
    <div class="container">
        <Breadcrumb
            :items="['User', isCreate ? 'user.form.title.create' : (isEdit ? 'user.form.title.edit' : 'user.form.title.view')]" />
        <a-form ref="formRef" layout="vertical" :model="formData" @submit="onSubmitClick">
            <a-space direction="vertical" :size="16">
                <a-card class="general-card" :bordered="false">
                    <template #title>
                        {{ $t(formTitle) }}
                    </template>
                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('user.form.label.username')" field="username"
                                :rules="[{ required: true, message: $t('user.form.validation.usernameRequired') }]">
                                <a-input v-model="formData.username" :placeholder="$t('user.form.placeholder.username')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item v-if="isCreate" :label="$t('user.form.label.password')" field="password"
                                :rules="[{ required: true, message: $t('user.form.validation.passwordRequired') }]">
                                <a-input-password v-model="formData.password"
                                    :placeholder="$t('user.form.placeholder.password')" />
                            </a-form-item>
                            <a-form-item v-else-if="isEdit" :label="$t('user.form.label.newPassword')" field="password">
                                <a-input-password v-model="formData.password"
                                    :placeholder="$t('user.form.placeholder.newPassword')" />
                            </a-form-item>
                            <a-form-item v-else :label="$t('user.form.label.password')">
                                <a-input value="********" disabled />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-row :gutter="16">
                        <a-col :span="12">
                            <a-form-item :label="$t('user.form.label.email')" field="email"
                                :rules="[{ required: true, message: $t('user.form.validation.emailRequired') }, { type: 'email', message: $t('user.form.validation.emailInvalid') }]">
                                <a-input v-model="formData.email" :placeholder="$t('user.form.placeholder.email')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                        <a-col :span="12">
                            <a-form-item :label="$t('user.form.label.telephone')" field="telephone">
                                <a-input v-model="formData.telephone"
                                    :placeholder="$t('user.form.placeholder.telephone')"
                                    :disabled="!isEdit && !isCreate" />
                            </a-form-item>
                        </a-col>
                    </a-row>

                    <a-form-item :label="$t('user.form.label.userPermissions')" field="userPermissions"
                        :rules="[{ required: true, message: $t('user.form.validation.userPermissionsRequired') }]">
                        <a-select v-model="formData.userPermissions"
                            :placeholder="$t('user.form.placeholder.userPermissions')" :disabled="!isEdit && !isCreate">
                            <a-option value="admin">{{ $t('user.form.option.admin') }}</a-option>
                            <a-option value="user">{{ $t('user.form.option.user') }}</a-option>
                            <a-option value="guest">{{ $t('user.form.option.guest') }}</a-option>
                        </a-select>
                    </a-form-item>

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
// 导入统一管理后的 API 函数
import { queryUserDetail, createUser, updateUserInfo, UserRecord } from '@/api/UserQ';
import { useUserStore } from '@/store';
import { useRoute, useRouter } from 'vue-router';

const userStore = useUserStore();
const formRef = ref<FormInstance>();
const { loading, setLoading } = useLoading();
const route = useRoute();
const router = useRouter();

// formData 现在直接匹配 UserRecord 接口，但 password 字段在编辑时将是空的
const formData = reactive<UserRecord>({
    username: '', // 对应 username
    password: '', // 初始为空
    email: '',
    telephone: '',
    userPermissions: 'user',
});

const usernoFromRoute = computed(() => route.params.userno as string | undefined);
const isCreate = computed(() => route.name === 'UserAdminCreate');
const isEdit = computed(() => route.name === 'UserAdminEdit');
const isView = computed(() => route.name === 'UserAdminView');
console.log('isCreate:', isCreate.value, 'isEdit:', isEdit.value, 'isView:', isView.value);
const formTitle = computed(() => {
    if (isCreate.value) return 'user.form.title.create';
    if (isEdit.value) return 'user.form.title.edit';
    if (isView.value) return 'user.form.title.view';
    return 'user.form.title.default';
});

// 获取用户详情数据
const fetchUserData = async (id: string) => {
    setLoading(true);
    try {
        const res = await queryUserDetail(id); // 使用统一的 API 函数

        const userData = res;
        // 填充表单数据，注意这里后端返回的 name 对应前端的 username
        // 并且 password 不回填
        formData.id = userData.id; // 存储 id/userno
        formData.number = userData.number;
        formData.username = userData.username;
        // formData.password = ''; // 密码字段不回填
        formData.email = userData.email;
        formData.telephone = userData.telephone;
        formData.userPermissions = userData.userPermissions;
        //   Message.success(res.message || '用户数据加载成功！');

    } catch (error: any) { // 使用 any 类型来捕获所有可能的错误
        Message.error(`获取用户详情出错: ${error.message || '未知错误'}`);
        console.error('Error fetching user data:', error);
        router.back();
    } finally {
        setLoading(false);
    }
};

const resetForm = () => {
    // 仅在创建模式下才完全重置，编辑模式下应保留原始userno，并重新加载
    if (isCreate.value) {
        Object.assign(formData, {
            name: '',
            password: '',
            email: '',
            telephone: '',
            userPermissions: 'user',
        });
        formRef.value?.resetFields();
    } else {
        // 编辑或查看模式，清空密码字段，其他数据不变
        formData.password = '';
        // 如果需要完全回到原始数据状态，可以重新调用 fetchUserData
        // if (usernoFromRoute.value) {
        //   fetchUserData(usernoFromRoute.value);
        // }
    }
};
// 监听路由参数变化，如果是编辑或查看模式则重新加载数据
watch(
    () => route.params.userno,
    (newVal) => {
        if ((isEdit.value || isView.value) && newVal) {
            fetchUserData(newVal as string);
        } else if (isCreate.value) {
            resetForm(); // 如果是创建模式，确保表单是空的
        }
    },
    { immediate: true } // 立即执行一次，以防组件在路由加载时就已经渲染
);

// 初始化时，如果当前是编辑或查看模式，且userno已存在，则加载数据
onMounted(() => {
    if ((isEdit.value || isView.value) && usernoFromRoute.value) {
        fetchUserData(usernoFromRoute.value);
    }
});

const onSubmitClick = async () => {
    const errors = await formRef.value?.validate();
    if (!errors) {
        setLoading(true);
        try {
            let res;
            // 准备要发送的数据
            const dataToSend: UserRecord = {
                username: formData.username,
                email: formData.email,
                telephone: formData.telephone,
                userPermissions: formData.userPermissions,
                // password 字段只在需要时包含
            };

            if (isCreate.value) {
                // 创建用户：password 是必填项
                dataToSend.password = formData.password;
                res = await createUser(dataToSend); // 使用统一的 API 函数
            } else if (isEdit.value) {
                // 编辑用户：如果 formData.password 有值，则表示用户输入了新密码，需要更新
                if (formData.password) {
                    dataToSend.password = formData.password; // 将新密码包含在更新请求中
                }
                // 对于更新，我们需要 userno
                if (!usernoFromRoute.value) {
                    Message.error('用户编号缺失，无法更新！');
                    setLoading(false);
                    return;
                }
                res = await updateUserInfo(usernoFromRoute.value, dataToSend); // 使用统一的 API 函数
            } else {
                // 不应该执行到这里，因为查看模式没有提交按钮
                return;
            }
            if (isEdit.value)
                router.push({ name: 'UserAdminList' }); // 提交成功后返回列表页
            else {
                Message.success('用户信息提交成功！'); // 创建成功的提示
                resetForm(); // 创建成功后重置表单
            }
        } catch (error: any) {
            console.error('提交用户信息失败:', error);
            Message.error(`操作失败: ${error.message || '未知错误'}`);
        } finally {
            setLoading(false);
        }
    } else {
        Message.warning('请检查并填写所有必填项！');
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
    padding: 0 20px 40px 20px;
    overflow: hidden;
}

.date-time-checkbox {
    margin-bottom: 8px;
    margin-right: 16px;
    vertical-align: middle;
}

:deep(.arco-select-view-disabled) {
    // opacity: 1!important;
    background-color: var(--color-bg-2)!important;
    border-color: var(--color-border-2)!important;
    cursor: default!important;
    pointer-events: none!important;
}

:deep(.arco-input-disabled) {
    // opacity: 1!important;
    background-color: var(--color-bg-2)!important;
    border-color: var(--color-border-2)!important;
    cursor: default!important;
    // pointer-events: none!important;
}


// :deep()

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