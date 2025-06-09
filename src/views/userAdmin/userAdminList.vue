<template>
  <div class="container">
    <Breadcrumb :items="['User', 'User.list']" />
    <a-card class="general-card" :title="$t('User.list')">
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
                  field="UserNo"
                  :label="$t('userAdmin.form.UserNo')"
                >
                  <a-input
                    v-model="formModel.UserNo"
                    :placeholder="
                      $t('userAdmin.form.UserNo.placeholder.notCreate')
                    "
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="UserName"
                  :label="$t('userAdmin.form.UserName')"
                >
                  <a-input
                    v-model="formModel.UserName"
                    :placeholder="$t('userAdmin.form.UserName.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item field="Email" :label="$t('userAdmin.form.Email')">
                  <a-input
                    v-model="formModel.Email"
                    :placeholder="$t('userAdmin.form.Email.placeholder')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="UserPermissions"
                  :label="$t('userAdmin.form.UserPermissions')"
                >
                  <a-select
                    v-model="formModel.UserPermissions"
                    :options="userPermissionsOptions"
                    :placeholder="$t('userAdmin.form.selectDefault')"
                  />
                </a-form-item>
              </a-col>
              <a-col :span="8">
                <a-form-item
                  field="Telephone"
                  :label="$t('userAdmin.form.Telephone')"
                >
                  <a-input
                    v-model="formModel.Telephone"
                    :placeholder="$t('userAdmin.form.Telephone.placeholder')"
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
          </a-space>
        </a-col>
        <a-col
          :span="12"
          style="display: flex; align-items: center; justify-content: end"
        >
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
          <a-tooltip :content="$t('userAdmin.actions.columnSetting')">
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
        row-key="UserNo"
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
        <template #UserPermissions="{ record }">
          {{ $t(`userAdmin.form.UserPermissions.${record.UserPermissions}`) }}
        </template>
        <template #operations="{ record }">
          <a-space :size="8">
            <a-button
              type="text"
              size="small"
              @click="handleView(record.UserNo)"
            >
              {{ $t('userAdmin.columns.operations.view') }}
            </a-button>
            <a-button
              v-permission="['admin']"
              type="text"
              size="small"
              @click="handleEdit(record.UserNo)"
            >
              {{ $t('userAdmin.columns.operations.edit') }}
            </a-button>
            <a-popconfirm
              :content="$t('userAdmin.message.confirmDelete')"
              @ok="handleDelete(record.UserNo)"
            >
              <a-button
                v-permission="['admin']"
                type="text"
                status="danger"
                size="small"
              >
                {{ $t('userAdmin.columns.operations.delete') }}
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
    queryUserList,
    deleteUser,
    type UserRecord,
    type UserParams,
  } from '@/api/userAdmin'; // <-- 导入新 API
  import { Pagination } from '@/types/global';
  import type { SelectOptionData } from '@arco-design/web-vue/es/select/interface';
  import type { TableColumnData } from '@arco-design/web-vue/es/table/interface';
  import cloneDeep from 'lodash/cloneDeep';
  import Sortable from 'sortablejs';
  import { useRouter } from 'vue-router';
  import { Message } from '@arco-design/web-vue';

  type SizeProps = 'mini' | 'small' | 'medium' | 'large';
  type Column = TableColumnData & { checked?: true };

  const generateFormModel = () => {
    return {
      UserNo: '',
      UserName: '',
      Email: '',
      UserPermissions: '',
      Telephone: '',
    };
  };
  const { loading, setLoading } = useLoading(true);
  const { t } = useI18n();
  const router = useRouter();

  const renderData = ref<UserRecord[]>([]);
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
      title: t('userAdmin.columns.UserNo'),
      dataIndex: 'UserNo',
    },
    {
      title: t('userAdmin.columns.UserName'),
      dataIndex: 'UserName',
    },
    {
      title: t('userAdmin.columns.UserPermissions'),
      dataIndex: 'UserPermissions',
      slotName: 'UserPermissions',
    },
    {
      title: t('userAdmin.columns.Email'),
      dataIndex: 'Email',
    },
    {
      title: t('userAdmin.columns.Telephone'),
      dataIndex: 'Telephone',
    },
    {
      title: t('userAdmin.columns.operations'),
      dataIndex: 'operations',
      slotName: 'operations',
      fixed: 'right',
      width: 180,
    },
  ]);

  // 用户权限选项，根据你的实际权限列表调整
  const userPermissionsOptions = computed<SelectOptionData[]>(() => [
    {
      label: t('userAdmin.form.UserPermissions.admin'),
      value: 'admin',
    },
    {
      label: t('userAdmin.form.UserPermissions.user'),
      value: 'user',
    },
    {
      label: t('userAdmin.form.UserPermissions.guest'),
      value: 'guest',
    },
  ]);

  const fetchData = async (
    params: UserParams = { current: 1, pageSize: 20 }
  ) => {
    setLoading(true);
    try {
      const apiResponse = await queryUserList(params);
      if (apiResponse) {
        renderData.value = apiResponse.list;
        console.log('获取用户列表成功:', renderData.value);
        pagination.current = params.current;
        pagination.total = apiResponse.total;
      } else {
        renderData.value = [];
        pagination.total = 0;
        console.warn('获取用户列表成功，但后端返回的业务数据为空。');
      }
    } catch (err: any) {
      console.error('获取用户列表失败:', err);
      Message.error(`获取用户列表出错: ${err.message || '未知错误'}`);
    } finally {
      setLoading(false);
    }
  };

  const search = () => {
    fetchData({
      ...basePagination,
      ...formModel.value,
    } as UserParams);
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

  const handleCreateUser = () => {
    router.push({
      name: 'UserAdminCreate',
    });
  };

  const handleView = (userno: string | undefined) => {
    if (!userno) {
      Message.error(t('userAdmin.message.idMissingForView'));
      return;
    }
    router.push({
      name: 'UserAdminView',
      params: { userno },
    });
  };
  const handleEdit = (userno: string | undefined) => {
    if (!userno) {
      Message.error(t('userAdmin.message.idMissingForEdit'));
      return;
    }
    router.push({
      name: 'UserAdminEdit',
      params: { userno },
    });
  };

  const handleDelete = async (userno: string | undefined) => {
    if (!userno) {
      Message.error(t('userAdmin.message.idMissingForDelete'));
      return;
    }
    setLoading(true);
    try {
      await deleteUser(userno);
      Message.success(t('userAdmin.message.deleteSuccess'));
      search();
    } catch (error: any) {
      console.error('删除用户失败:', error);
      Message.error(
        `${t('userAdmin.message.deleteFail')}: ${error.message || '未知错误'}`
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
    name: 'UserAdminTable',
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
