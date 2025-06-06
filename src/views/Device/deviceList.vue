<template>
    <div class="container">
        <Breadcrumb :items="['device', 'device.list']" />
        <a-card class="general-card" :title="$t('device.list')">
            <a-row>
                <a-col :flex="1">
                    <a-form :model="formModel" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }"
                        label-align="left">
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item field="DeviceNo" :label="$t('device.form.label.deviceNo')">
                                    <a-input v-model="formModel.DeviceNo"
                                        :placeholder="$t('device.form.placeholder.deviceNo')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="DeviceName" :label="$t('device.form.label.deviceName')">
                                    <a-input v-model="formModel.DeviceName"
                                        :placeholder="$t('device.form.placeholder.deviceName')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="DeviceUsage" :label="$t('device.form.label.deviceUsage')">
                                    <a-input v-model="formModel.DeviceUsage"
                                        :placeholder="$t('device.form.placeholder.deviceUsage')" />
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
                            {{ $t('device.form.search') }}
                        </a-button>
                        <a-button @click="reset">
                            <template #icon>
                                <icon-refresh />
                            </template>
                            {{ $t('device.form.reset') }}
                        </a-button>
                    </a-space>
                </a-col>
            </a-row>
            <a-divider style="margin-top: 0" />
            <a-row style="margin-bottom: 16px">
                <a-col :span="12">
                    <a-space>
                        <a-button type="primary" @click="handleCreateDevice">
                            <template #icon>
                                <icon-plus />
                            </template>
                            {{ $t('device.operation.create') }}
                        </a-button>
                    </a-space>
                </a-col>
                <a-col :span="12" style="display: flex; align-items: center; justify-content: end">
                    <a-tooltip :content="$t('device.actions.refresh')">
                        <div class="action-icon" @click="search">
                            <icon-refresh size="18" />
                        </div>
                    </a-tooltip>
                    <a-dropdown @select="handleSelectDensity">
                        <a-tooltip :content="$t('device.actions.density')">
                            <div class="action-icon"><icon-line-height size="18" /></div>
                        </a-tooltip>
                        <template #content>
                            <a-doption v-for="item in densityList" :key="item.value" :value="item.value"
                                :class="{ active: item.value === size }">
                                <span>{{ item.name }}</span>
                            </a-doption>
                        </template>
                    </a-dropdown>
                    <a-tooltip :content="$t('device.actions.columnSetting')">
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
            <a-table row-key="DeviceNo" :loading="loading" :pagination="pagination"
                :columns="(cloneColumns as TableColumnData[])" :data="renderData" :bordered="false" :size="size"
                @page-change="onPageChange">
                <template #index="{ rowIndex }">
                    {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
                </template>
                <template #DStartTime="{ record }">
                    {{ formatDateTime(record.DStartTime) }}
                </template>
                <template #DMT="{ record }">
                    {{ formatDateTime(record.DMT) }}
                </template>
                <template #DStopTime="{ record }">
                    {{ formatDateTime(record.DStopTime) }}
                </template>
                <template #operations="{ record }">
                    <a-space :size="8">
                        <a-button type="text" size="small" @click="handleView(record.DeviceNo)">
                            {{ $t('device.columns.operations.view') }}
                        </a-button>
                        <a-button v-permission="['admin']" type="text" size="small"
                            @click="handleEdit(record.DeviceNo)">
                            {{ $t('device.columns.operations.edit') }}
                        </a-button>
                        <a-popconfirm @ok="handleDelete(record.DeviceNo)" :content="$t('device.message.confirmDelete')">
                            <a-button v-permission="['admin']" type="text" status="danger" size="small">
                                {{ $t('device.columns.operations.delete') }}
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
import { queryDeviceList, deleteDevice, DeviceRecord, DeviceParams } from '@/api/device'; // 导入新的API
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
        DeviceNo: '',
        DeviceName: '',
        DeviceUsage: '',
    };
};
const { loading, setLoading } = useLoading(true);
const { t } = useI18n();
const router = useRouter();

const renderData = ref<DeviceRecord[]>([]);
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
    { name: t('device.size.mini'), value: 'mini' },
    { name: t('device.size.small'), value: 'small' },
    { name: t('device.size.medium'), value: 'medium' },
    { name: t('device.size.large'), value: 'large' },
]);
const columns = computed<TableColumnData[]>(() => [
    {
        title: t('device.columns.index'),
        dataIndex: 'index',
        slotName: 'index',
    },
    {
        title: t('device.columns.DeviceNo'),
        dataIndex: 'DeviceNo',
    },
    {
        title: t('device.columns.DeviceName'),
        dataIndex: 'DeviceName',
    },
    {
        title: t('device.columns.DeviceUsage'),
        dataIndex: 'DeviceUsage',
    },
    {
        title: t('device.columns.DStartTime'),
        dataIndex: 'DStartTime',
        slotName: 'DStartTime',
    },
    {
        title: t('device.columns.DMT'),
        dataIndex: 'DMT',
        slotName: 'DMT',
    },
    {
        title: t('device.columns.DStopTime'),
        dataIndex: 'DStopTime',
        slotName: 'DStopTime',
    },
    {
        title: t('device.columns.operations'),
        dataIndex: 'operations',
        slotName: 'operations',
        fixed: 'right',
        width: 180,
    },
]);

const formatDateTime = (dateTimeString?: string | null) => {
    if (!dateTimeString) {
        return ''; // 如果是 null 或 undefined 或空字符串，返回空
    }
    // 假设是 ISO 8601 格式 (YYYY-MM-DDTHH:mm:ss)
    // 替换 'T' 为空格
    return dateTimeString.replace('T', ' ');
};

const fetchData = async (params: DeviceParams = { current: 1, pageSize: 20 }) => {
    setLoading(true);
    try {
        const apiResponse = await queryDeviceList(params);
        if (apiResponse) {
            renderData.value = apiResponse.list;
            pagination.current = params.current;
            pagination.total = apiResponse.total;
        } else {
            renderData.value = [];
            pagination.total = 0;
            console.warn('获取设备列表成功，但后端返回的业务数据为空。');
        }
    } catch (err: any) {
        console.error('获取设备列表失败:', err);
    } finally {
        setLoading(false);
    }
};

const search = () => {
    fetchData({
        ...basePagination,
        ...formModel.value,
    } as unknown as DeviceParams);
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

const handleCreateDevice = () => {
    router.push({
        name: 'DeviceAdminCreate',
    });
};

const handleView = (deviceNo: string | undefined) => {
    if (!deviceNo) {
        Message.error(t('device.message.idMissingForView'));
        return;
    }
    router.push({
        name: 'DeviceAdminView',
        params: { deviceNo },
    });
};

const handleEdit = (deviceNo: string | undefined) => {
    if (!deviceNo) {
        Message.error(t('device.message.idMissingForEdit'));
        return;
    }
    router.push({
        name: 'DeviceAdminEdit',
        params: { deviceNo },
    });
};

const handleDelete = async (deviceNo: string | undefined) => {
    if (!deviceNo) {
        Message.error(t('device.message.idMissingForDelete'));
        return;
    }
    setLoading(true);
    try {
        await deleteDevice(deviceNo);
        Message.success(t('device.message.deleteSuccess'));
        search();
    } catch (error: any) {
        console.error('删除设备失败:', error);
        Message.error(`${t('device.message.deleteFail')}: ${error.message || '未知错误'}`);
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
    name: 'DeviceList',
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