<template>
  <div class="container">
    <Breadcrumb :items="['experiment', 'experiment.list']" />
    <a-card class="general-card" :title="$t('experiment.list')">
      <!-- ... (搜索表单部分不变) ... -->
      <a-divider style="margin-top: 0" />
      <a-row style="margin-bottom: 16px">
        <a-col :span="12">
          <a-space>
            <a-button type="primary" @click="handleCreateExperiment">
              <template #icon>
                <icon-plus />
              </template>
              {{ $t('experiment.operation.create') }}
            </a-button>
            <a-button type="primary" @click="handleConductExperiment">
              <template #icon>
                <icon-play-arrow />
              </template>
              {{ $t('experiment.operation.conduct') }}
            </a-button>
          </a-space>
        </a-col>
        <a-col
          :span="12"
          style="display: flex; align-items: center; justify-content: end"
        >
          <a-tooltip :content="$t('experiment.actions.refresh')">
            <div class="action-icon" @click="search">
              <icon-refresh size="18" />
            </div>
          </a-tooltip>
          <a-dropdown @select="handleSelectDensity">
            <a-tooltip :content="$t('experiment.actions.density')">
              <div class="action-icon"><icon-line-height size="18" /></div>
            </a-tooltip>
            <template #content>
              <a-doption
                v-for="item in densityList"
                :key="item.value"
                :value="item.value"
                :class="{ active: item.value === size }"
              >
                <span>{{ item.name }}</span>
              </a-doption>
            </template>
          </a-dropdown>
          <a-tooltip :content="$t('experiment.actions.columnSetting')">
            <a-popover
              trigger="click"
              position="bl"
              @popup-visible-change="popupVisibleChange"
            >
              <div class="action-icon"><icon-settings size="18" /></div>
              <template #content>
                <div id="tableSetting">
                  <div
                    v-for="(item, index) in showColumns"
                    :key="item.dataIndex"
                    class="setting"
                  >
                    <div style="margin-right: 4px; cursor: move">
                      <icon-drag-arrow />
                    </div>
                    <div>
                      <a-checkbox
                        v-model="item.checked"
                        @change="
                          handleChange($event, item as TableColumnData, index)
                        "
                      >
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
      <a-table
        row-key="ExperimentNo"
        :loading="loading"
        :pagination="pagination"
        :columns="(cloneColumns as TableColumnData[])"
        :data="renderData"
        :bordered="false"
        :size="size"
        @page-change="onPageChange"
      >
        <template #index="{ rowIndex }">
          {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
        </template>
        <!-- 时间字段格式化 -->
        <template #StartTime="{ record }">
          {{ formatTime(record.StartTime) }}
        </template>
        <template #EndTime="{ record }">
          {{ formatTime(record.EndTime) }}
        </template>
        <!-- 移除 GelTime 插槽 -->
        <!-- <template #GelTime="{ record }">
                    {{ formatTime(record.GelTime) }}
                </template> -->
        <template #operations="{ record }">
          <a-space :size="8">
            <a-button
              type="text"
              size="small"
              @click="handleView(record.ExperimentNo)"
            >
              {{ $t('experiment.columns.operations.view') }}
            </a-button>
            <a-button
              v-permission="['admin']"
              type="text"
              size="small"
              @click="handleEdit(record.ExperimentNo)"
            >
              {{ $t('experiment.columns.operations.edit') }}
            </a-button>
            <a-popconfirm
              :content="$t('experiment.message.confirmDelete')"
              @ok="handleDelete(record.ExperimentNo)"
            >
              <a-button
                v-permission="['admin']"
                type="text"
                status="danger"
                size="small"
              >
                {{ $t('experiment.columns.operations.delete') }}
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
  import {
    queryExperimentList,
    deleteExperiment,
    ExperimentRecord,
    ExperimentParams,
  } from '@/api/experiment';
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
      ExperimentNo: '',
      MaterialCode: '',
      ProtocolNo: '',
      UserNo: '',
    };
  };
  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  const router = useRouter();

  const renderData = ref<ExperimentRecord[]>([]);
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
    { name: t('experiment.size.mini'), value: 'mini' },
    { name: t('experiment.size.small'), value: 'small' },
    { name: t('experiment.size.medium'), value: 'medium' },
    { name: t('experiment.size.large'), value: 'large' },
  ]);
  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('experiment.columns.index'),
      dataIndex: 'index',
      slotName: 'index',
    },
    {
      title: t('experiment.columns.ExperimentNo'),
      dataIndex: 'ExperimentNo',
    },
    {
      title: t('experiment.columns.MaterialCode'),
      dataIndex: 'MaterialCode',
    },
    {
      title: t('experiment.columns.HeatError'),
      dataIndex: 'HeatError',
    },
    {
      title: t('experiment.columns.MixError'),
      dataIndex: 'MixError',
    },
    {
      title: t('experiment.columns.StartTime'),
      dataIndex: 'StartTime',
      slotName: 'StartTime',
    },
    {
      title: t('experiment.columns.EndTime'),
      dataIndex: 'EndTime',
      slotName: 'EndTime',
    },
    // 移除 GelTime 列定义
    // {
    //     title: t('experiment.columns.GelTime'),
    //     dataIndex: 'GelTime',
    //     slotName: 'GelTime',
    // },
    {
      title: t('experiment.columns.ProtocolNo'),
      dataIndex: 'ProtocolNo',
    },
    {
      title: t('experiment.columns.UserNo'),
      dataIndex: 'UserNo',
    },
    {
      title: t('experiment.columns.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      fixed: 'right',
      width: 180,
    },
  ]);

  // 格式化时间字符串 HH:MM:SS
  const formatTime = (timeString?: string | null) => {
    console.log('formatTime called with:', timeString);
    if (!timeString) {
      return '';
    }
    return timeString;
  };

  const fetchData = async (
    params: ExperimentParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const apiResponse = await queryExperimentList(params);
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
    } as unknown as ExperimentParams);
  };
  const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
  };

  fetchData();
  const reset = () => {
    formModel.value = generateFormModel();
    search();
  };

  const handleSelectDensity = (
    val: string | number | Record<string, any> | undefined
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

  const handleCreateExperiment = () => {
    router.push({
      name: 'ExperimentAdminCreate',
    });
  };

  const handleConductExperiment = () => {
    // 新增的执行实验按钮处理
    router.push({
      name: 'ExperimentAdminConduct',
    });
  };

  const handleView = (experimentNo: string | undefined) => {
    if (!experimentNo) {
      Message.error(t('experiment.message.idMissingForView'));
      return;
    }
    router.push({
      name: 'ExperimentAdminView',
      params: { experimentNo },
    });
  };

  const handleEdit = (experimentNo: string | undefined) => {
    if (!experimentNo) {
      Message.error(t('experiment.message.idMissingForEdit'));
      return;
    }
    router.push({
      name: 'ExperimentAdminEdit',
      params: { experimentNo },
    });
  };

  const handleDelete = async (experimentNo: string | undefined) => {
    if (!experimentNo) {
      Message.error(t('experiment.message.idMissingForDelete'));
      return;
    }
    setLoading(true);
    try {
      await deleteExperiment(experimentNo);
      Message.success(t('experiment.message.deleteSuccess'));
      search();
    } catch (error: any) {
      console.error('删除实验失败:', error);
      Message.error(
        `${t('experiment.message.deleteFail')}: ${error.message || '未知错误'}`
      );
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
    name: 'ExperimentList',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
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
