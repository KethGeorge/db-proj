<template>
  <a-modal
    :visible="visible"
    :title="title"
    :width="1200"
    :footer="false"
    unmount-on-close
    @cancel="handleCancel"
  >
    <a-table
      row-key="ModificationID"
      :loading="loading"
      :pagination="pagination"
      :columns="columns"
      :data="logData"
      :bordered="false"
      size="small"
      :scroll="{ y: 400 }"
      @page-change="onPageChange"
    >
      <template #OperationTime="{ record }">
        {{ dayjs(record.OperationTime).format('YYYY-MM-DD HH:mm:ss') }}
      </template>
    </a-table>
  </a-modal>
</template>

<script lang="ts" setup>
  import { ref, reactive, computed, watch } from 'vue';
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import {
    queryModificationListByUser,
    type ModificationRecord,
  } from '@/api/modification';
  import { Pagination } from '@/types/global';
  import type { TableColumnData } from '@arco-design/web-vue';
  import dayjs from 'dayjs';

  interface Props {
    visible: boolean;
    userNo: string;
    userName?: string;
  }

  const props = defineProps<Props>();
  const emit = defineEmits(['update:visible']);

  const { t } = useI18n();
  const { loading, setLoading } = useLoading(false);

  const logData = ref<ModificationRecord[]>([]);
  const pagination = reactive<Pagination>({
    current: 1,
    pageSize: 10,
    total: 0,
    showTotal: true,
  });

  const title = computed(() =>
    t('userAdmin.logViewer.title', {
      name: props.userName || props.userNo,
    })
  );

  const columns = computed<TableColumnData[]>(() => [
    {
      title: t('audit.columns.OperationTime'),
      dataIndex: 'OperationTime',
      slotName: 'OperationTime',
      width: 170,
    },
    {
      title: t('audit.columns.OperationType'),
      dataIndex: 'OperationType',
      width: 100,
    },
    {
      title: t('audit.columns.Operator'), // 统一叫“操作者”
      dataIndex: 'OperatorUserName',
      width: 130,
    },
    {
      title: t('audit.columns.EntityType'),
      dataIndex: 'EntityType',
      width: 130,
    },
    {
      title: t('audit.columns.EntityID'),
      dataIndex: 'EntityID',
      width: 150,
    },
    {
      title: t('audit.columns.FieldName'),
      dataIndex: 'FieldName',
      width: 150,
    },
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

  const fetchData = async (c = 1, ps = 10) => {
    if (!props.userNo) return;
    setLoading(true);
    try {
      const { list, total } = await queryModificationListByUser(props.userNo, {
        current: c,
        pageSize: ps,
      });
      logData.value = list;
      pagination.total = total;
      pagination.current = c;
      pagination.pageSize = ps;
    } catch (error) {
      console.error('获取用户修改记录失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const onPageChange = (current: number) => {
    fetchData(current, pagination.pageSize);
  };

  const handleCancel = () => {
    emit('update:visible', false);
  };

  watch(
    () => props.visible,
    (newVal) => {
      if (newVal) {
        // 每次打开时重置并重新加载第一页
        pagination.current = 1;
        fetchData(1, pagination.pageSize);
      }
    }
  );
</script>
