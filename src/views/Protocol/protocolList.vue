<template>
    <div class="container">
        <Breadcrumb :items="['protocol', 'protocol.list']" />
        <a-card class="general-card" :title="$t('protocol.list')">
            <a-row>
                <a-col :flex="1">
                    <a-form :model="formModel" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }"
                        label-align="left">
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item field="ProtocolNo" :label="$t('protocol.form.label.ProtocolNo')">
                                    <a-input v-model="formModel.ProtocolNo"
                                        :placeholder="$t('protocol.form.placeholder.ProtocolNo')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="MaterialCode" :label="$t('protocol.form.label.MaterialCode')">
                                    <a-input v-model="formModel.MaterialCode"
                                        :placeholder="$t('protocol.form.placeholder.MaterialCode')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="UserNo" :label="$t('protocol.form.label.UserNo')">
                                    <a-input v-model="formModel.UserNo"
                                        :placeholder="$t('protocol.form.placeholder.UserNo')" />
                                </a-form-item>
                            </a-col>
                            <!-- 其他字段可以根据需要添加到搜索条件 -->
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
                            {{ $t('protocol.form.search') }}
                        </a-button>
                        <a-button @click="reset">
                            <template #icon>
                                <icon-refresh />
                            </template>
                            {{ $t('protocol.form.reset') }}
                        </a-button>
                    </a-space>
                </a-col>
            </a-row>
            <a-divider style="margin-top: 0" />
            <a-row style="margin-bottom: 16px">
                <a-col :span="12">
                    <a-space>
                        <a-button type="primary" @click="handleCreateProtocol">
                            <template #icon>
                                <icon-plus />
                            </template>
                            {{ $t('protocol.operation.create') }}
                        </a-button>
                    </a-space>
                </a-col>
                <a-col :span="12" style="display: flex; align-items: center; justify-content: end">
                    <a-tooltip :content="$t('protocol.actions.refresh')">
                        <div class="action-icon" @click="search">
                            <icon-refresh size="18" />
                        </div>
                    </a-tooltip>
                    <a-dropdown @select="handleSelectDensity">
                        <a-tooltip :content="$t('protocol.actions.density')">
                            <div class="action-icon"><icon-line-height size="18" /></div>
                        </a-tooltip>
                        <template #content>
                            <a-doption v-for="item in densityList" :key="item.value" :value="item.value"
                                :class="{ active: item.value === size }">
                                <span>{{ item.name }}</span>
                            </a-doption>
                        </template>
                    </a-dropdown>
                    <a-tooltip :content="$t('protocol.actions.columnSetting')">
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
            <a-table row-key="ProtocolNo" :loading="loading" :pagination="pagination"
                :columns="(cloneColumns as TableColumnData[])" :data="renderData" :bordered="false" :size="size"
                @page-change="onPageChange">
                <template #index="{ rowIndex }">
                    {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
                </template>
                <template #operations="{ record }">
                    <a-space :size="8">
                        <a-button type="text" size="small" @click="handleView(record.ProtocolNo)">
                            {{ $t('protocol.columns.operations.view') }}
                        </a-button>
                        <a-button v-permission="['admin']" type="text" size="small" @click="handleEdit(record.ProtocolNo)">
                            {{ $t('protocol.columns.operations.edit') }}
                        </a-button>
                        <a-popconfirm @ok="handleDelete(record.ProtocolNo)" :content="$t('protocol.message.confirmDelete')">
                            <a-button v-permission="['admin']" type="text" status="danger" size="small">
                                {{ $t('protocol.columns.operations.delete') }}
                            </a-button>
                        </a-popconfirm>
                    </a-space>
                </template>
            </a-table>
        </a-card>
    </div>
</template>

<script lang="ts" setup>
import { computed, ref, reactive, watch, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import useLoading from '@/hooks/loading';
import { queryProtocolList, deleteProtocol, ProtocolRecord, ProtocolParams } from '@/api/protocol'; // 导入新的API
import { Pagination } from '@/types/global';
import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
import cloneDeep from 'lodash/cloneDeep';
import Sortable from 'sortablejs';
import { useRouter } from 'vue-router';
import { Message } from '@arco-design/web-vue';

type SizeProps = 'mini' | 'small' | 'medium' | 'large';
type Column = TableColumnData & { checked?: true };

const generateFormModel = () => {
    return {
        ProtocolNo: '',
        NSN: '',
        MaterialCode: '',
        UserNo: '',
        // 其他浮点数字段不作为搜索条件
    };
};
const { loading, setLoading } = useLoading(true);
const { t } = useI18n();
const router = useRouter();

const renderData = ref<ProtocolRecord[]>([]);
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
    { name: t('protocol.size.mini'), value: 'mini' },
    { name: t('protocol.size.small'), value: 'small' },
    { name: t('protocol.size.medium'), value: 'medium' },
    { name: t('protocol.size.large'), value: 'large' },
]);
const columns = computed<TableColumnData[]>(() => [
    {
        title: t('protocol.columns.index'),
        dataIndex: 'index',
        slotName: 'index',
    },
    {
        title: t('protocol.columns.ProtocolNo'),
        dataIndex: 'ProtocolNo',
    },
    {
        title: t('protocol.columns.NSN'),
        dataIndex: 'NSN',
    },
    {
        title: t('protocol.columns.SHT'),
        dataIndex: 'SHT',
    },
    {
        title: t('protocol.columns.SMS'),
        dataIndex: 'SMS',
    },
    {
        title: t('protocol.columns.MixingAngle'),
        dataIndex: 'MixingAngle',
    },
    {
        title: t('protocol.columns.MixingRadius'),
        dataIndex: 'MixingRadius',
    },
    {
        title: t('protocol.columns.MeasurementInterval'),
        dataIndex: 'MeasurementInterval',
    },
    {
        title: t('protocol.columns.MaterialCode'),
        dataIndex: 'MaterialCode',
    },
    {
        title: t('protocol.columns.UserNo'),
        dataIndex: 'UserNo',
    },
    {
        title: t('protocol.columns.operations'),
        dataIndex: 'operations',
        slotName: 'operations',
        fixed: 'right',
        width: 180,
    },
]);


const fetchData = async (params: ProtocolParams = { current: 1, pageSize: 20 }) => {
    setLoading(true);
    try {
        const apiResponse = await queryProtocolList(params);
        if (apiResponse) {
            renderData.value = apiResponse.list;
            pagination.current = params.current;
            pagination.total = apiResponse.total;
        } else {
            renderData.value = [];
            pagination.total = 0;
            console.warn('获取协议列表成功，但后端返回的业务数据为空。');
        }
    } catch (err: any) {
        console.error('获取协议列表失败:', err);
    } finally {
        setLoading(false);
    }
};

const search = () => {
    fetchData({
        ...basePagination,
        ...formModel.value,
    } as unknown as ProtocolParams);
};
const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
};

fetchData();
const reset = () => {
    formModel.value = generateFormModel();
    search();
};

const handleSelectDensity = (val: string | number | Record<string, any> | undefined) => {
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
            if (el) {
                const sortable = new Sortable(el, {
                    onEnd(e: any) {
                        const { oldIndex, newIndex } = e;
                        exchangeArray(cloneColumns.value, oldIndex, newIndex);
                        exchangeArray(showColumns.value, oldIndex, newIndex);
                    },
                });
            }
        });
    }
};

const handleCreateProtocol = () => {
    router.push({
        name: 'ProtocolAdminCreate',
    });
};

const handleView = (protocolNo: string | undefined) => {
    if (!protocolNo) {
        Message.error(t('protocol.message.idMissingForView'));
        return;
    }
    router.push({
        name: 'ProtocolAdminView',
        params: { protocolNo },
    });
};

const handleEdit = (protocolNo: string | undefined) => {
    if (!protocolNo) {
        Message.error(t('protocol.message.idMissingForEdit'));
        return;
    }
    router.push({
        name: 'ProtocolAdminEdit',
        params: { protocolNo },
    });
};

const handleDelete = async (protocolNo: string | undefined) => {
    if (!protocolNo) {
        Message.error(t('protocol.message.idMissingForDelete'));
        return;
    }
    setLoading(true);
    try {
        await deleteProtocol(protocolNo);
        Message.success(t('protocol.message.deleteSuccess'));
        search();
    } catch (error: any) {
        console.error('删除协议失败:', error);
        Message.error(`${t('protocol.message.deleteFail')}: ${error.message || '未知错误'}`);
    } finally {
        setLoading(false);
    }
};

watch(
    () => columns.value,
    (val) => {
        cloneColumns.value = cloneDeep(val);
        cloneColumns.value.forEach((item) => {
            item.checked = true;
        });
        showColumns.value = cloneDeep(cloneColumns.value);
    },
    { deep: true, immediate: true }
);
</script>

<script lang="ts">
export default {
    name: 'ProtocolList',
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