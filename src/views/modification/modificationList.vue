<template>
  <div class="container">
    <Breadcrumb :items="['menu.audit', 'menu.audit.log']" />
    <a-card class="general-card" :title="$t('audit.list.title')">
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
                <!-- ==================== 这里是主要修改点 ==================== -->
                <a-form-item
                  field="EntityType"
                  :label="$t('audit.columns.EntityType')"
                >
                  <!-- 修改后: 使用 a-select 组件 -->
                  <a-select
                    v-model="formModel.EntityType"
                    :options="entityTypeOptions"
                    :placeholder="$t('audit.form.placeholder.EntityType')"
                    allow-clear
                  />
                  <!-- 
                    修改前:
                    <a-input v-model="formModel.EntityType" :placeholder="$t('audit.form.placeholder.EntityType')" />
                  -->
                </a-form-item>
                <!-- ==================== 修改结束 ==================== -->
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="EntityID"
                  :label="$t('audit.columns.EntityID')"
                >
                  <a-input
                    v-model="formModel.EntityID"
                    :placeholder="$t('audit.form.placeholder.EntityID')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item field="UserNo" :label="$t('audit.columns.UserNo')">
                  <SearchSelect
                    v-model="formModel.UserNo"
                    :api-function="searchUsers"
                    key-field="UserNo"
                    label-field="UserName"
                    :placeholder="$t('audit.form.placeholder.UserNo')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="OperationType"
                  :label="$t('audit.columns.OperationType')"
                >
                  <a-select
                    v-model="formModel.OperationType"
                    :placeholder="$t('audit.form.placeholder.OperationType')"
                    allow-clear
                  >
                    <a-option value="INSERT">INSERT</a-option>
                    <a-option value="UPDATE">UPDATE</a-option>
                    <a-option value="DELETE">DELETE</a-option>
                  </a-select>
                </a-form-item>
              </a-col>
            </a-row>
          </a-form>
        </a-col>
        <a-divider style="height: 84px" direction="vertical" />
        <a-col :flex="'86px'" style="text-align: right">
          <a-space direction="vertical" :size="18">
            <a-button type="primary" @click="search">
              <template #icon><icon-search /></template>
              {{ $t('audit.form.search') }}
            </a-button>
            <a-button @click="reset">
              <template #icon><icon-refresh /></template>
              {{ $t('audit.form.reset') }}
            </a-button>
          </a-space>
        </a-col>
      </a-row>
      <a-divider style="margin-top: 0" />

      <!-- 列表 -->
      <a-table
        row-key="ModificationID"
        :loading="loading"
        :pagination="pagination"
        :columns="(columns as TableColumnData[])"
        :data="renderData"
        :bordered="false"
        @page-change="onPageChange"
      >
        <template #index="{ rowIndex }">
          {{ rowIndex + 1 + (pagination.current - 1) * pagination.pageSize }}
        </template>
        <template #OperationTime="{ record }">
          {{ dayjs(record.OperationTime).format('YYYY-MM-DD HH:mm:ss') }}
        </template>
      </a-table>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
  import { computed, ref, reactive } from 'vue';
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import {
    queryModificationList,
    ModificationRecord,
    ModificationParams,
  } from '@/api/modification';
  import { Pagination } from '@/types/global';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import dayjs from 'dayjs';
  import SearchSelect from '@/components/searchSelect/index.vue';
  import { searchUsers } from '@/api/userAdmin';

  // 1. 定义实体类型选项数组
  const entityTypeOptions = [
    'Protocol',
    'User',
    'Device',
    'Material',
    'National_Standard',
    'Experiment',
  ];

  const generateFormModel = () => {
    return {
      // 2. 将 EntityType 的初始值改为 undefined
      EntityType: undefined,
      EntityID: '',
      UserNo: undefined,
      OperationType: undefined,
    };
  };

  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  const renderData = ref<ModificationRecord[]>([]);
  const formModel = ref(generateFormModel());

  const basePagination: Pagination = {
    current: 1,
    pageSize: 20,
    showTotal: true,
  };
  const pagination = reactive({
    ...basePagination,
  });

  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('audit.columns.index'),
      dataIndex: 'index',
      slotName: 'index',
      width: 80,
    },
    {
      title: t('audit.columns.OperationTime'),
      dataIndex: 'OperationTime',
      slotName: 'OperationTime',
      width: 180,
    },
    {
      title: t('audit.columns.OperationType'),
      dataIndex: 'OperationType',
      width: 120,
    },
    {
      title: t('audit.columns.Operator'),
      dataIndex: 'OperatorUserName',
      width: 120,
    },
    {
      title: t('audit.columns.EntityType'),
      dataIndex: 'EntityType',
      width: 150,
    }, // 可以适当加宽
    { title: t('audit.columns.EntityID'), dataIndex: 'EntityID', width: 150 },
    { title: t('audit.columns.FieldName'), dataIndex: 'FieldName', width: 150 },
    {
      title: t('audit.columns.OldValue'),
      dataIndex: 'OldValue',
      ellipsis: true,
      tooltip: true,
    },
    {
      title: t('audit.columns.NewValue'),
      dataIndex: 'NewValue',
      ellipsis: true,
      tooltip: true,
    },
  ]);

  const fetchData = async (
    params: ModificationParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const { list, total } = await queryModificationList(params);
      renderData.value = list;
      pagination.current = params.current;
      pagination.total = total;
    } catch (err) {
      // you can report use
    } finally {
      setLoading(false);
    }
  };

  const search = () => {
    fetchData({
      ...basePagination,
      ...formModel.value,
    } as unknown as ModificationParams);
  };

  const onPageChange = (current: number) => {
    fetchData({
      ...formModel.value,
      current,
      pageSize: pagination.pageSize,
    } as unknown as ModificationParams);
  };

  fetchData();

  const reset = () => {
    formModel.value = generateFormModel();
    search();
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }
</style>
