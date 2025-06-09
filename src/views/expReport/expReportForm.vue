<template>
  <div class="container">
    <Breadcrumb :items="['experiment', 'menu.experimentAdmin.report']" />
    <a-spin :loading="loading" style="width: 100%">
      <a-card class="general-card">
        <template #title>
          {{ $t('experiment.report.title') }}
        </template>
        <template #extra>
          <a-button type="primary" @click="goBack">{{
            $t('groupForm.back')
          }}</a-button>
        </template>

        <!-- 主报告信息 -->
        <a-descriptions
          v-if="reportData?.reportDetails"
          :data="formatMainDetails(reportData.reportDetails)"
          :column="2"
          bordered
          layout="inline-vertical"
          table-layout="fixed"
          class="section-margin"
        />
        <a-empty v-else />

        <!-- HEC 加热实验 -->
        <a-card
          :title="$t('experiment.report.hecTitle')"
          class="section-margin"
        >
          <a-descriptions
            v-if="reportData?.hecData"
            :data="formatHecData(reportData.hecData)"
            :column="2"
            bordered
            layout="inline-vertical"
            table-layout="fixed"
          />
          <a-empty v-else>
            <template #description>
              {{ $t('experiment.report.noHecData') }}
            </template>
          </a-empty>
        </a-card>

        <!-- MEC 搅拌实验 -->
        <a-card
          :title="$t('experiment.report.mecTitle')"
          class="section-margin"
        >
          <a-descriptions
            v-if="reportData?.mecData"
            :data="formatMecData(reportData.mecData)"
            :column="2"
            bordered
            layout="inline-vertical"
            table-layout="fixed"
          />
          <a-empty v-else>
            <template #description>
              {{ $t('experiment.report.noMecData') }}
            </template>
          </a-empty>
        </a-card>

        <!-- MTEC 测定实验 -->
        <a-card :title="$t('experiment.report.mtecTitle')">
          <a-descriptions
            v-if="reportData?.mtecData"
            :data="formatMtecData(reportData.mtecData)"
            :column="2"
            bordered
            layout="inline-vertical"
            table-layout="fixed"
          />
          <a-empty v-else>
            <template #description>
              {{ $t('experiment.report.noMtecData') }}
            </template>
          </a-empty>
        </a-card>
      </a-card>
    </a-spin>
  </div>
</template>

<script lang="ts" setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import useLoading from '@/hooks/loading';
  import { Message } from '@arco-design/web-vue';
  import {
    queryExperimentReport,
    type ExperimentReportRecord,
    type ReportDetailsRecord,
    type HECRecord,
    type MECRecord,
    type MTECRecord,
  } from '@/api/expReport';

  const route = useRoute();
  const router = useRouter();
  const { t } = useI18n();
  const { loading, setLoading } = useLoading(true);

  const reportData = ref<ExperimentReportRecord | null>(null);

  const fetchReportData = async (experimentNo: string) => {
    setLoading(true);
    try {
      const res = await queryExperimentReport(experimentNo);
      reportData.value = res;
    } catch (error: any) {
      Message.error(t('experiment.report.fetchFail'));
      console.error('获取实验报告失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatMainDetails = (data: ReportDetailsRecord) => [
    {
      label: t('experiment.report.label.ExperimentCode'),
      value: data.ExperimentCode,
    },
    {
      label: t('experiment.report.label.ExperimentNo'),
      value: data.ExperimentNo,
    },
    {
      label: t('experiment.report.label.ExperimentName'),
      value: data.ExperimentName,
    },
    {
      label: t('experiment.report.label.ExperimentalStatus'),
      value: data.ExperimentalStatus,
    },
  ];

  const formatHecData = (data: HECRecord) => [
    { label: t('experiment.report.label.HEC'), value: data.HEC },
    {
      label: t('experiment.report.label.Temperature'),
      value: data.Temperature,
    },
    { label: t('experiment.report.label.Time1'), value: data.Time1 },
    { label: t('experiment.report.label.SafeArea'), value: data.SafeArea },
  ];

  const formatMecData = (data: MECRecord) => [
    { label: t('experiment.report.label.MEC'), value: data.MEC },
    {
      label: t('experiment.report.label.HeightError'),
      value: data.HeightError,
    },
    { label: t('experiment.report.label.PlainError'), value: data.PlainError },
    { label: t('experiment.report.label.ErrorArea'), value: data.ErrorArea },
    { label: t('experiment.report.label.SpeedError'), value: data.SpeedError },
    { label: t('experiment.report.label.Time2'), value: data.Time2 },
  ];

  const formatMtecData = (data: MTECRecord) => [
    { label: t('experiment.report.label.MTEC'), value: data.MTEC },
    { label: t('experiment.report.label.PhotoPath'), value: data.PhotoPath },
    {
      label: t('experiment.report.label.IsGel'),
      value: data.IsGel
        ? t('experiment.report.yes')
        : t('experiment.report.no'),
    },
    { label: t('experiment.report.label.Time3'), value: data.Time3 },
  ];

  onMounted(() => {
    const experimentNo = route.params.experimentNo as string;
    if (experimentNo) {
      fetchReportData(experimentNo);
    }
  });

  const goBack = () => {
    router.push({ name: 'ExperimentReportList' });
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 20px;
  }

  .section-margin {
    margin-bottom: 20px;
  }
</style>
