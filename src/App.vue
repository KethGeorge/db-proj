<template>
  <a-config-provider :locale="locale">
    <router-view :key="$route.fullPath" />
    <global-setting />
  </a-config-provider>
</template>

<script lang="ts" setup>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  import enUS from '@arco-design/web-vue/es/locale/lang/en-us';
  import zhCN from '@arco-design/web-vue/es/locale/lang/zh-cn';
  import GlobalSetting from '@/components/global-setting/index.vue';
  import useLocale from '@/hooks/locale';
  
    const route = useRoute(); // <-- 添加这一行

  const { currentLocale } = useLocale();
  const locale = computed(() => {
    switch (currentLocale.value) {
      case 'zh-CN':
        return zhCN;
      case 'en-US':
        return enUS;
      default:
        return enUS;
    }
  });
</script>
