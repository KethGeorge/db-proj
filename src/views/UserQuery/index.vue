<template>
    <div class="container">
        <Breadcrumb :items="['User', 'User.list']" />
        <a-card class="general-card" :title="$t('User.list')">
            <a-row>
                <a-col :flex="1">
                    <a-form :model="formModel" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }"
                        label-align="left">
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item field="userno" :label="$t('userAdmin.form.userno')">
                                    <a-input v-model="formModel.userno"
                                        :placeholder="$t('userAdmin.form.userno.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="username" :label="$t('userAdmin.form.username')">
                                    <a-input v-model="formModel.username"
                                        :placeholder="$t('userAdmin.form.username.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="email" :label="$t('userAdmin.form.email')">
                                    <a-input v-model="formModel.email"
                                        :placeholder="$t('userAdmin.form.email.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="userPermissions" :label="$t('userAdmin.form.userPermissions')">
                                    <a-select v-model="formModel.userPermissions" :options="userPermissionsOptions"
                                        :placeholder="$t('userAdmin.form.selectDefault')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="telephone" :label="$t('userAdmin.form.telephone')">
                                    <a-input v-model="formModel.telephone"
                                        :placeholder="$t('userAdmin.form.telephone.placeholder')" />
                                </a-form-item>
                            </a-col>
                        </a-row>
                    </a-form>
                </a-col>
                <a-divider style="height: 84px" direction="vertical" />
                <a-col :flex="'86px'" style="text-align: right">
                    <a-space direction="vertical" :size="18">
                        <a-button type="primary" @click="search">
                            <template #icon>
                                <icon-search />
                            </template>
                            {{ $t('userAdmin.form.search') }}
                        </a-button>
                        <a-button @click="reset">
                            <template #icon>
                                <icon-refresh />
                            </template>
                            {{ $t('userAdmin.form.reset') }}
                        </a-button>
                    </a-space>
                </a-col>
            </a-row>
            <a-divider style="margin-top: 0" />
            <a-row style="margin-bottom: 16px">
                <a-col :span="12">
                    <a-space>
                        <a-button type="primary" @click="handleCreateUser">
                            <template #icon>
                                <icon-plus />
                            </template>
                            {{ $t('userAdmin.operation.create') }}
                        </a-button>
                        <!-- <a-upload action="/">
                            <template #upload-button>
                                <a-button>
                                    {{ $t('userAdmin.operation.import') }}
                                </a-button>
                            </template>
                        </a-upload> -->
                    </a-space>
                </a-col>
                <a-col :span="12" style="display: flex; align-items: center; justify-content: end">
<!--                     <a-button>
                        <template #icon>
                            <icon-download />
                        </template>
                        {{ $t('userAdmin.operation.download') }}
                    </a-button> -->
                    <a-tooltip :content="$t('userAdmin.actions.refresh')">
                        <div class="action-icon" @click="search">
                            <icon-refresh size="18" />
                        </div>
                    </a-tooltip>
                    <a-dropdown @select="handleSelectDensity">
                        <a-tooltip :content="$t('userAdmin.actions.density')">
                            <div class="action-icon"><icon-line-height size="18" /></div>
                        </a-tooltip>
                        <template #content>
                            <a-doption v-for="item in densityList" :key="item.value" :value="item.value"
                                :class="{ active: item.value === size }">
                                <span>{{ item.name }}</span>
                            </a-doption>
                        </template>
                    </a-dropdown>
                    <a-tooltip :content="$t('userAdmin.actions.columnSetting')">
                        <a-popover trigger="click" position="bl" @popup-visible-change="popupVisibleChange">
                            <div class="action-icon"><icon-settings size="18" /></div>
                            <template #content>
                                <div id="tableSetting">
                                    <div v-for="(item, index) in showColumns" :key="item.dataIndex" class="setting">
                                        <div style="margin-right: 4px; cursor: move">
                                            <icon-drag-arrow />
                                        </div>
                                        <div>
                                            <a-checkbox v-model="item.checked" @change="
                                                handleChange($event, item as TableColumnData, index)
                                                ">
                                            </a-checkbox>
                                        </div>
                                        <div class="title">
                                            {{ item.title === '#' ? '序列号' : item.title }}
                                        </div>
                                    </div>
                                </div>
                            </template>
                        </a-popover>
                    </a-tooltip>
                </a-col>
            </a-row>
            <a-table row-key="id" :loading="loading" :pagination="pagination"
                :columns="(cloneColumns as TableColumnData[])" :data="renderData" :bordered="false" :size="size"
                @page-change="onPageChange">
                <template #index="{ rowIndex }">
                    {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
                </template>
                <template #userPermissions="{ record }">
                    {{ $t(`userAdmin.form.userPermissions.${record.userPermissions}`) }}
                </template>
                <template #operations="{ record }">
                    <a-button type="text" size="small" @click="handleView(record.id)">
                        {{ $t('userAdmin.columns.operations.view') }}
                    </a-button>
                    <a-button v-permission="['admin']" type="text" size="small" @click="handleEdit(record.id)">
                        {{ $t('userAdmin.columns.operations.edit') }}
                    </a-button>
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script lang="ts" setup>
import { computed, ref, reactive, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import useLoading from '@/hooks/loading';
// 导入新的用户查询 API，注意路径已更改
import { queryUserList, UserRecord, UserParams } from '@/api/UserQ';
import { Pagination } from '@/types/global';
import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
import cloneDeep from 'lodash/cloneDeep';
import Sortable from 'sortablejs';
import { useRouter } from 'vue-router'; // 修改：导入 useRouter
import { Message } from '@arco-design/web-vue'; // 修改：引入 Message 组件

type SizeProps = 'mini' | 'small' | 'medium' | 'large';
type Column = TableColumnData & { checked?: true };

const generateFormModel = () => {
    return {
        userno: '',
        username: '',
        email: '',
        userPermissions: '',
        telephone: '',
    };
};
const { loading, setLoading } = useLoading(true);
const { t } = useI18n();
const router = useRouter();

const renderData = ref<UserRecord[]>([]); // 修改类型为 UserRecord
const formModel = ref(generateFormModel());
const cloneColumns = ref<Column[]>([]);
const showColumns = ref<Column[]>([]);

const size = ref<SizeProps>('medium');

const basePagination: Pagination = {
    current: 1,
    pageSize: 20,
};
const pagination = reactive({
    ...basePagination,
});
const densityList = computed(() => [
    {
        name: t('userAdmin.size.mini'),
        value: 'mini',
    },
    {
        name: t('userAdmin.size.small'),
        value: 'small',
    },
    {
        name: t('userAdmin.size.medium'),
        value: 'medium',
    },
    {
        name: t('userAdmin.size.large'),
        value: 'large',
    },
]);
const columns = computed<TableColumnData[]>(() => [
    {
        title: t('userAdmin.columns.index'),
        dataIndex: 'index',
        slotName: 'index',
    },
    {
        title: t('userAdmin.columns.userno'),
        dataIndex: 'number', // 映射 UserNo 到 number
    },
    {
        title: t('userAdmin.columns.username'),
        dataIndex: 'name', // 映射 UserName 到 name
    },
    {
        title: t('userAdmin.columns.userPermissions'),
        dataIndex: 'userPermissions',
        slotName: 'userPermissions',
    },
    {
        title: t('userAdmin.columns.email'),
        dataIndex: 'email',
    },
    {
        title: t('userAdmin.columns.telephone'),
        dataIndex: 'telephone',
    },
    {
        title: t('userAdmin.columns.operations'),
        dataIndex: 'operations',
        slotName: 'operations',
    },
]);

// 用户权限选项，根据你的实际权限列表调整
const userPermissionsOptions = computed<SelectOptionData[]>(() => [
    {
        label: t('userAdmin.form.userPermissions.admin'),
        value: 'admin',
    },
    {
        label: t('userAdmin.form.userPermissions.user'),
        value: 'user',
    },
    {
        label: t('userAdmin.form.userPermissions.guest'),
        value: 'guest',
    },
]);

const fetchData = async (params: UserParams = { current: 1, pageSize: 20 }) => {
    setLoading(true);
    try {
        // 这里的 response 是 AxiosResponse<HttpResponse<UserListRes>> 类型
        const response = await queryUserList(params);
        // apiResponse 是 HttpResponse<UserListRes> 类型
        const apiResponse = response;

        // 拦截器已经处理了 code !== 20000 的情况并抛出错误，
        // 所以如果代码执行到这里，apiResponse.code 必然是 20000。
        // 但是，需要检查 apiResponse.data 是否存在，因为后端可能返回 code=20000 但 data=null
        if (apiResponse) { // apiResponse.data 是 UserListRes 类型
            renderData.value = apiResponse.list;
            pagination.current = params.current; // 这个来自 params，没问题
            pagination.total = apiResponse.total;
        } else {
            // 如果 apiResponse.data 为空（即后端返回 code 20000 但无实际业务数据）
            // 此时列表应为空，总数应为 0
            renderData.value = [];
            pagination.total = 0;
            console.warn('获取用户列表成功，但后端返回的业务数据为空。');
            // 如果需要，也可以给一个信息提示：
            // Message.info(apiResponse.message || '未找到用户列表数据。');
        }
    } catch (err: any) { // 捕获拦截器抛出的错误或网络错误
        console.error('获取用户列表失败:', err);
        // 错误消息通常已经在拦截器中显示了（通过 Message.error），这里可以不再重复显示
        // 如果需要更细致的错误处理或本地化，可以在这里添加
        // Message.error(`获取用户列表出错: ${err.message || '未知错误'}`); 
    } finally {
        setLoading(false);
    }
};

const search = () => {
    fetchData({
        ...basePagination,
        ...formModel.value,
    } as unknown as UserParams); // 确保类型正确
};
const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
};

fetchData();
const reset = () => {
    formModel.value = generateFormModel();
};

const handleSelectDensity = (
    val: string | number | Record<string, any> | undefined,
    e: Event
) => {
    size.value = val as SizeProps;
};

const handleChange = (
    checked: boolean | (string | boolean | number)[],
    column: Column,
    index: number
) => {
    if (!checked) {
        cloneColumns.value = showColumns.value.filter(
            (item) => item.dataIndex !== column.dataIndex
        );
    } else {
        cloneColumns.value.splice(index, 0, column);
    }
};

const exchangeArray = <T extends Array<any>>(
    array: T,
    beforeIdx: number,
    newIdx: number,
    isDeep = false
): T => {
    const newArray = isDeep ? cloneDeep(array) : array;
    if (beforeIdx > -1 && newIdx > -1) {
        newArray.splice(
            beforeIdx,
            1,
            newArray.splice(newIdx, 1, newArray[beforeIdx]).pop()
        );
    }
    return newArray;
};

const popupVisibleChange = (val: boolean) => {
    if (val) {
        nextTick(() => {
            const el = document.getElementById('tableSetting') as HTMLElement;
            const sortable = new Sortable(el, {
                onEnd(e: any) {
                    const { oldIndex, newIndex } = e;
                    exchangeArray(cloneColumns.value, oldIndex, newIndex);
                    exchangeArray(showColumns.value, oldIndex, newIndex);
                },
            });
        });
    }
};

// 修改：新增跳转到用户新增页的函数
const handleCreateUser = () => {
  router.push({
    name: 'UserAdminCreate', // 对应路由配置中的 name
  });
};

// 修改：新增跳转到用户详情页的函数


const handleView = (userno: string | undefined) => {
  if (!userno) {
    Message.error(t('userAdmin.message.idMissingForView')); // 修改：使用国际化提示
    return;
  }
  router.push({
    name: 'UserAdminView', // 对应路由配置中的 name
    params: { userno }, // 传递动态参数 userno
  });
};
const handleEdit = (userno: string | undefined) => {
  if (!userno) {
    Message.error(t('userAdmin.message.idMissingForEdit')); // 修改：使用国际化提示
    return;
  }
  console.log('Navigating to UserAdminEdit with userno:', userno);
  router.push({
    name: 'UserAdminEdit', // 对应路由配置中的 name
    params: { userno }, // 传递动态参数 userno
  });
};

watch(
    () => columns.value,
    (val) => {
        cloneColumns.value = cloneDeep(val);
        cloneColumns.value.forEach((item, index) => {
            item.checked = true;
        });
        showColumns.value = cloneDeep(cloneColumns.value);
    },
    { deep: true, immediate: true }
);
</script>

<script lang="ts">
export default {
    name: 'UserAdminTable',
};
</script>

<style scoped lang="less">
.container {
    padding: 0 20px 20px 20px;
}

:deep(.arco-table-th) {
    &:last-child {
        .arco-table-th-item-title {
            margin-left: 16px;
        }
    }
}

.action-icon {
    margin-left: 12px;
    cursor: pointer;
}

.active {
    color: #0960bd;
    background-color: #e3f4fc;
}

.setting {
    display: flex;
    align-items: center;
    width: 200px;

    .title {
        margin-left: 12px;
        cursor: pointer;
    }
}
</style>