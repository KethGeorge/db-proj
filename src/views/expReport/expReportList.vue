<template>
  <div class="container">
    <Breadcrumb :items="['menu.report', 'menu.report.list']" />
    <a-card class="general-card" :title="$t('menu.report.list')">
      <!-- 搜索表单 -->
      <a-row>
        <a-col :flex="1">
          <a-form
            :model="formModel"
            :label-col-props="{ span: 6 }"
            :wrapper-col-props="{ span: 18 }"
            label-align="left"
          >
            <a-row :gutter="16">
              <a-col :span="8">
                <a-form-item
                  field="ExperimentCode"
                  :label="$t('report.list.label.ExperimentCode')"
                >
                  <a-input
                    v-model="formModel.ExperimentCode"
                    :placeholder="$t('report.list.placeholder.ExperimentCode')"
                    allow-clear
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="ExperimentNo"
                  :label="$t('report.list.label.ExperimentNo')"
                >
                  <a-input
                    v-model="formModel.ExperimentNo"
                    :placeholder="$t('report.list.placeholder.ExperimentNo')"
                    allow-clear
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="ExperimentName"
                  :label="$t('report.list.label.ExperimentName')"
                >
                  <a-input
                    v-model="formModel.ExperimentName"
                    :placeholder="$t('report.list.placeholder.ExperimentName')"
                    allow-clear
                  />
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
        <a-divider style="height: 84px" direction="vertical" />
        <a-col :flex="'86px'" style="text-align: right">
          <a-space direction="vertical" :size="18">
            <a-button type="primary" @click="search">
              <template #icon> <icon-search /> </template>
              {{ $t('report.list.search') }}
            </a-button>
            <a-button @click="reset">
              <template #icon> <icon-refresh /> </template>
              {{ $t('report.list.reset') }}
            </a-button>
          </a-space>
        </a-col>
      </a-row>
      <a-divider style="margin-top: 0" />
      <!-- 表格 -->
      <a-table
        row-key="ExperimentCode"
        :loading="loading"
        :pagination="pagination"
        :columns="columns"
        :data="renderData"
        :bordered="false"
        @page-change="onPageChange"
      >
        <template #index="{ rowIndex }">
          {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
        </template>
        <template #operations="{ record }">
          <a-button type="text" size="small" @click="handleView(record)">
            {{ $t('report.list.operations.view') }}
          </a-button>
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, computed } from 'vue';
  import { useI18n } from 'vue-i18n';
  import { useRouter } from 'vue-router';
  import useLoading from '@/hooks/loading';
  import { Pagination } from '@/types/global';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import {
    queryReportList,
    type ReportListParams,
    type ReportListItem,
  } from '@/api/expReport';

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);
  const router = useRouter();

  const generateFormModel = () => ({
    ExperimentCode: '',
    ExperimentNo: '',
    ExperimentName: '',
    ExperimentalStatus: '',
  });

  const formModel = ref(generateFormModel());
  const renderData = ref<ReportListItem[]>([]);
  const basePagination: Pagination = { current: 1, pageSize: 20 };
  const pagination = reactive({ ...basePagination, total: 0 });

  const columns = computed<TableColumnData[]>(() => [
    { title: '#', dataIndex: 'index', slotName: 'index' },
    {
      title: t('report.list.columns.ExperimentCode'),
      dataIndex: 'ExperimentCode',
    },
    {
      title: t('report.list.columns.ExperimentNo'),
      dataIndex: 'ExperimentNo',
    },
    {
      title: t('report.list.columns.ExperimentName'),
      dataIndex: 'ExperimentName',
    },
    {
      title: t('report.list.columns.ExperimentalStatus'),
      dataIndex: 'ExperimentalStatus',
    },
    {
      title: t('report.list.columns.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
    },
  ]);

  const fetchData = async (
    params: ReportListParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const { list, total } = await queryReportList(params);
      renderData.value = list;
      pagination.current = params.current;
      pagination.total = total;
    } catch (err) {
      // you can report error
    } finally {
      setLoading(false);
    }
  };

  const search = () => {
    fetchData({
      ...basePagination,
      ...formModel.value,
    } as ReportListParams);
  };

  const reset = () => {
    formModel.value = generateFormModel();
    search();
  };

  const onPageChange = (current: number) => {
    fetchData({ ...basePagination, current });
  };

  const handleView = (record: ReportListItem) => {
    router.push({
      name: 'ExperimentReportView',
      params: { experimentNo: record.ExperimentNo },
    });
  };

  fetchData();
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
