<template>
    <div class="container">
        <Breadcrumb :items="['NationalStandard', 'NationalStandard.list']" />
        <a-card class="general-card" :title="$t('nationalStandard.list')">
            <a-row>
                <a-col :flex="1">
                    <a-form :model="formModel" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }"
                        label-align="left">
                        <a-row :gutter="16">
                            <a-col :span="8">
                                <a-form-item field="NSN" :label="$t('nationalStandard.form.NSN')">
                                    <a-input v-model="formModel.NSN"
                                        :placeholder="$t('nationalStandard.form.NSN.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="StandardName" :label="$t('nationalStandard.form.StandardName')">
                                    <a-input v-model="formModel.StandardName"
                                        :placeholder="$t('nationalStandard.form.StandardName.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <a-col :span="8">
                                <a-form-item field="MaterialCode" :label="$t('nationalStandard.form.MaterialCode')">
                                    <a-input v-model="formModel.MaterialCode"
                                        :placeholder="$t('nationalStandard.form.MaterialCode.placeholder')" />
                                </a-form-item>
                            </a-col>
                            <!-- Description 字段可能较长，不适合作为搜索条件，此处省略 -->
                            <!-- <a-col :span="8">
                                <a-form-item field="Description" :label="$t('nationalStandard.form.Description')">
                                    <a-input v-model="formModel.Description"
                                        :placeholder="$t('nationalStandard.form.Description.placeholder')" />
                                </a-form-item>
                            </a-col> -->
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
                            {{ $t('nationalStandard.form.search') }}
                        </a-button>
                        <a-button @click="reset">
                            <template #icon>
                                <icon-refresh />
                            </template>
                            {{ $t('nationalStandard.form.reset') }}
                        </a-button>
                    </a-space>
                </a-col>
            </a-row>
            <a-divider style="margin-top: 0" />
            <a-row style="margin-bottom: 16px">
                <a-col :span="12">
                    <a-space>
                        <a-button type="primary" @click="handleCreateStandard">
                            <template #icon>
                                <icon-plus />
                            </template>
                            {{ $t('nationalStandard.operation.create') }}
                        </a-button>
                        <!-- <a-upload action="/">
                            <template #upload-button>
                                <a-button>
                                    {{ $t('nationalStandard.operation.import') }}
                                </a-button>
                            </template>
                        </a-upload> -->
                    </a-space>
                </a-col>
                <a-col :span="12" style="display: flex; align-items: center; justify-content: end">
                    <!-- <a-button>
                        <template #icon>
                            <icon-download />
                        </template>
                        {{ $t('nationalStandard.operation.download') }}
                    </a-button> -->
                    <a-tooltip :content="$t('nationalStandard.actions.refresh')">
                        <div class="action-icon" @click="search">
                            <icon-refresh size="18" />
                        </div>
                    </a-tooltip>
                    <a-dropdown @select="handleSelectDensity">
                        <a-tooltip :content="$t('nationalStandard.actions.density')">
                            <div class="action-icon"><icon-line-height size="18" /></div>
                        </a-tooltip>
                        <template #content>
                            <a-doption v-for="item in densityList" :key="item.value" :value="item.value"
                                :class="{ active: item.value === size }">
                                <span>{{ item.name }}</span>
                            </a-doption>
                        </template>
                    </a-dropdown>
                    <a-tooltip :content="$t('nationalStandard.actions.columnSetting')">
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
            <a-table row-key="NSN" :loading="loading" :pagination="pagination"
                :columns="(cloneColumns as TableColumnData[])" :data="renderData" :bordered="false" :size="size"
                @page-change="onPageChange">
                <template #index="{ rowIndex }">
                    {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
                </template>
                <template #operations="{ record }">
                    <a-space :size="8">
                        <a-button type="text" size="small" @click="handleView(record.NSN)">
                            {{ $t('nationalStandard.columns.operations.view') }}
                        </a-button>
                        <a-button v-permission="['admin']" type="text" size="small" @click="handleEdit(record.NSN)">
                            {{ $t('nationalStandard.columns.operations.edit') }}
                        </a-button>
                        <a-popconfirm @ok="handleDelete(record.NSN)"
                            :content="$t('nationalStandard.message.confirmDelete')">
                            <a-button v-permission="['admin']" type="text" status="danger" size="small">
                                {{ $t('nationalStandard.columns.operations.delete') }}
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
// 导入新的国家标准查询 API
import { queryNationalStandardList, deleteNationalStandard, NationalStandardRecord, NationalStandardParams } from '@/api/NationalStandard';
import { Pagination } from '@/types/global'; // 假设有这个类型
import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
import cloneDeep from 'lodash/cloneDeep';
import Sortable from 'sortablejs';
import { useRouter } from 'vue-router';
import { Message, Modal } from '@arco-design/web-vue';

type SizeProps = 'mini' | 'small' | 'medium' | 'large';
type Column = TableColumnData & { checked?: true };

const generateFormModel = () => {
    return {
        NSN: '',
        StandardName: '',
        Description: '',
        MaterialCode: '',
    };
};
const { loading, setLoading } = useLoading(true);
const { t } = useI18n();
const router = useRouter();

const renderData = ref<NationalStandardRecord[]>([]);
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
        name: t('nationalStandard.size.mini'),
        value: 'mini',
    },
    {
        name: t('nationalStandard.size.small'),
        value: 'small',
    },
    {
        name: t('nationalStandard.size.medium'),
        value: 'medium',
    },
    {
        name: t('nationalStandard.size.large'),
        value: 'large',
    },
]);
const columns = computed<TableColumnData[]>(() => [
    {
        title: t('nationalStandard.columns.index'),
        dataIndex: 'index',
        slotName: 'index',
    },
    {
        title: t('nationalStandard.columns.NSN'),
        dataIndex: 'NSN',
    },
    {
        title: t('nationalStandard.columns.StandardName'),
        dataIndex: 'StandardName',
    },
    {
        title: t('nationalStandard.columns.Description'),
        dataIndex: 'Description',
    },
    {
        title: t('nationalStandard.columns.MaterialCode'),
        dataIndex: 'MaterialCode',
    },
    {
        title: t('nationalStandard.columns.operations'),
        dataIndex: 'operations',
        slotName: 'operations',
        fixed: 'right', // 操作列固定在右侧
        width: 180, // 增加宽度以容纳更多按钮
    },
]);


const fetchData = async (params: NationalStandardParams = { current: 1, pageSize: 20 }) => {
    setLoading(true);
    try {
        const apiResponse = await queryNationalStandardList(params);

        if (apiResponse) {
            renderData.value = apiResponse.list;
            pagination.current = params.current;
            pagination.total = apiResponse.total;
        } else {
            renderData.value = [];
            pagination.total = 0;
            console.warn('获取国家标准列表成功，但后端返回的业务数据为空。');
        }
    } catch (err: any) {
        console.error('获取国家标准列表失败:', err);
    } finally {
        setLoading(false);
    }
};

const search = () => {
    fetchData({
        ...basePagination,
        ...formModel.value,
    } as unknown as NationalStandardParams);
};
const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
};

fetchData();
const reset = () => {
    formModel.value = generateFormModel();
    search(); // 重置后重新搜索
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

const handleCreateStandard = () => {
    router.push({
        name: 'NationalStandardAdminCreate',
    });
};

const handleView = (nsn: string | undefined) => {
    if (!nsn) {
        Message.error(t('nationalStandard.message.idMissingForView'));
        return;
    }
    router.push({
        name: 'NationalStandardAdminView',
        params: { nsn },
    });
};

const handleEdit = (nsn: string | undefined) => {
    if (!nsn) {
        Message.error(t('nationalStandard.message.idMissingForEdit'));
        return;
    }
    router.push({
        name: 'NationalStandardAdminEdit',
        params: { nsn },
    });
};

const handleDelete = async (nsn: string | undefined) => {
    if (!nsn) {
        Message.error(t('nationalStandard.message.idMissingForDelete'));
        return;
    }
    setLoading(true);
    try {
        await deleteNationalStandard(nsn);
        Message.success(t('nationalStandard.message.deleteSuccess'));
        search(); // 删除成功后刷新列表
    } catch (error: any) {
        console.error('删除国家标准失败:', error);
        Message.error(`${t('nationalStandard.message.deleteFail')}: ${error.message || '未知错误'}`);
    } finally {
        setLoading(false);
    }
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
    name: 'NationalStandardTable',
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