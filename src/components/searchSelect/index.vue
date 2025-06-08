<template>
  <a-select
    :model-value="modelValue"
    :placeholder="placeholder"
    :disabled="disabled"
    :allow-clear="true"
    :show-search="true"
    :filter-option="false"
    :allow-search="true"
    @search="handleSearch"
    @change="handleChange"
  >
    <a-option
      v-for="item in options"
      :key="item[keyField]"
      :value="item[keyField]"
    >
      {{ item[labelField] }}
      <span v-if="descriptionField && item[descriptionField]">
        ({{ item[descriptionField] }})
      </span>
    </a-option>
  </a-select>
</template>

<script lang="ts" setup>
  import { ref, computed, watch, onMounted } from 'vue';
  import { Message } from '@arco-design/web-vue';

  // 定义组件的 Props
  interface Props {
    modelValue: string | number | undefined | null; // v-model 绑定的值 (当前选中的ID)
    apiFunction: (params: { query: string; limit?: number }) => Promise<any[]>; // 接受一个异步搜索函数
    keyField: string; // 选项中作为 value 的字段名 (如 'MaterialCode', 'UserNo')
    labelField: string; // 选项中作为显示文本的字段名 (如 'MaterialName', 'UserName')
    descriptionField?: string; // 选项中作为额外描述的字段名 (如 'NSN')
    placeholder?: string;
    disabled?: boolean;
  }

  const props = defineProps<Props>();
  const emit = defineEmits(['update:modelValue']); // 声明触发 update:modelValue 事件

  const options = ref<any[]>([]); // 存储搜索结果选项
  const searchTimeout = ref<number | null>(null); // 用于防抖
  const searchValue = ref<string>(''); // 用于控制 a-select 内部的搜索框的值

  // --- 搜索逻辑 ---
  const handleSearch = async (currentSearchValue: string) => {
    console.log(
      'SearchSelect: handleSearch triggered with:',
      currentSearchValue
    );
    if (searchTimeout.value) {
      clearTimeout(searchTimeout.value);
    }
    options.value = []; // 每次搜索前清空旧选项
    if (!currentSearchValue) {
      return;
    }
    searchTimeout.value = setTimeout(async () => {
      try {
        const result = await props.apiFunction({
          query: currentSearchValue,
          limit: 10,
        }); // 调用传入的API函数
        options.value = result;
        console.log('SearchSelect: API search results:', result);
      } catch (error) {
        console.error(`SearchSelect: 搜索失败 (${props.labelField}):`, error);
        Message.error(`搜索${props.labelField}失败`);
        options.value = [];
      }
    }, 300) as unknown as number;
  };

  // --- 值改变 (用户选中或清空) 逻辑 ---
  const handleChange = (
    value:
      | string
      | number
      | Record<string, any>
      | undefined
      | (string | number | Record<string, any>)[]
      | boolean
  ) => {
    if (Array.isArray(value) || typeof value === 'boolean') {
      // 非单选字符串/数字值，或者布尔值 (非预期)
      emit('update:modelValue', undefined); // 视为清空
      searchValue.value = ''; // 清空搜索框
      options.value = []; // 清空选项
      return;
    }

    // 正常单选值：string | number | Record<string, any> | undefined
    if (value === undefined || value === null || value === '') {
      emit('update:modelValue', undefined); // 清空 modelValue
      searchValue.value = ''; // 清空搜索框
      options.value = []; // 清空选项
    } else {
      // value 是选中项的实际值 (如 MaterialCode)
      emit('update:modelValue', value); // 更新 modelValue

      // 尝试找到选中项的显示文本，并更新 searchValue
      const selectedOption = options.value.find(
        (item) => item[props.keyField] === value
      );
      if (selectedOption) {
        searchValue.value = `${selectedOption[props.labelField]} ${
          selectedOption[props.descriptionField as string]
            ? `(${selectedOption[props.descriptionField as string]})`
            : ''
        }`;
      } else {
        // 如果选中了一个值，但这个值不在当前 options 中 (例如初始加载时，或在搜索后选择的，但 options 随后被清空)
        // 需要去后端加载其显示文本。或者暂时显示其代码。
        // 这里的逻辑应在 onMounted/watch modelValue 变化时处理更健壮
        searchValue.value = value.toString();
      }
    }
  };

  // --- 内部输入框值变化逻辑 ---
  const handleInputValueChange = (currentSearchValue: string) => {
    searchValue.value = currentSearchValue;
    handleSearch(currentSearchValue); // 触发搜索
  };

  // --- 初始加载和 modelValue 变化时，同步 searchValue 的显示文本 ---
  watch(
    () => props.modelValue,
    async (newVal) => {
      if (newVal !== undefined && newVal !== null && newVal !== '') {
        // 如果 modelValue 有值，且当前 searchValue 与其不匹配，或者 options 中没有对应的显示文本
        // (例如在编辑模式下初次加载时)
        const currentOptionInOptions = options.value.find(
          (item) => item[props.keyField] === newVal
        );
        if (
          !currentOptionInOptions ||
          searchValue.value !==
            `${currentOptionInOptions[props.labelField]} ${
              currentOptionInOptions[props.descriptionField as string]
                ? `(${
                    currentOptionInOptions[props.descriptionField as string]
                  })`
                : ''
            }`
        ) {
          // 只有当 options 中没有当前选中项，或者 searchValue 显示不正确时，才去搜索并更新
          try {
            // 调用 apiFunction 精确搜索当前值，并将其添加到 options
            const result = await props.apiFunction({
              query: newVal.toString(),
              limit: 1,
            });
            if (result.length > 0 && result[0][props.keyField] === newVal) {
              // 确保 options 列表包含这个已选中的项
              if (
                !options.value.some(
                  (item) => item[props.keyField] === result[0][props.keyField]
                )
              ) {
                options.value.push(result[0]);
              }
              // 更新 searchValue 以显示格式化文本
              searchValue.value = `${result[0][props.labelField]} ${
                result[0][props.descriptionField as string]
                  ? `(${result[0][props.descriptionField as string]})`
                  : ''
              }`;
            } else {
              // 如果 initial value 在后端找不到，清空绑定值和 searchValue
              emit('update:modelValue', undefined);
              searchValue.value = '';
            }
          } catch (e) {
            console.error(
              `SearchSelect: 加载初始值失败 (${props.keyField}):`,
              e
            );
            // 仅当加载失败时才清空，否则保持原样 (可能用户手动输入的)
            emit('update:modelValue', undefined);
            searchValue.value = '';
          }
        }
      } else {
        // 如果 modelValue 为空，确保 searchValue 也为空
        searchValue.value = '';
        options.value = [];
      }
    },
    { immediate: true }
  ); // 立即执行一次，处理组件初次加载时的 modelValue
</script>

<style scoped lang="less">
  /* 可以添加一些通用样式 */
</style>
