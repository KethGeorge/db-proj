<template>
  <div class="container">
    <Breadcrumb :items="['experiment', 'experiment.operation.conduct']" />
    <a-card class="general-card" :title="$t('experiment.conduct.title')">
      <div class="experiment-area">
        <!-- 阶段 1: 静态图片展示 -->
        <div v-if="currentStage === 'prepare'" class="preparation-stage">
          <h3>{{ $t('experiment.conduct.preparationTitle') }}</h3>
          <div class="image-gallery">
            <img
              :src="staticImage1"
              alt="Preparation Image 1"
              class="experiment-image"
            />
            <img
              :src="staticImage2"
              alt="Preparation Image 2"
              class="experiment-image"
            />
          </div>
          <a-button
            type="primary"
            :loading="loading"
            class="start-button"
            @click="startExperiment"
          >
            <template #icon>
              <icon-play-arrow />
            </template>
            {{ $t('experiment.conduct.startButton') }}
          </a-button>
        </div>

        <!-- 阶段 2: 视频/GIF 播放 -->
        <div v-else-if="currentStage === 'running'" class="running-stage">
          <h3>{{ $t('experiment.conduct.runningTitle') }}</h3>
          <div class="media-player">
            <video
              v-if="mediaType === 'video'"
              ref="videoPlayer"
              :src="experimentVideo"
              controls
              autoplay
              muted
              class="experiment-media"
              @ended="onMediaEnded"
            >
              Your browser does not support the video tag.
            </video>
            <img
              v-else-if="mediaType === 'gif'"
              :src="experimentGif"
              alt="Experiment GIF"
              class="experiment-media"
              @load="onMediaLoaded"
            />
            <a-spin
              v-if="loadingMedia"
              tip="加载中..."
              style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
              "
            />
          </div>
          <a-button
            type="text"
            status="danger"
            :loading="loading"
            class="end-button"
            @click="endExperimentImmediately"
          >
            <!-- 修复 type="status" -->
            <template #icon>
              <icon-stop />
            </template>
            {{ $t('experiment.conduct.endButtonImmediate') }}
          </a-button>
        </div>

        <!-- 阶段 3: 实验数据上传 -->
        <div v-else-if="currentStage === 'data_entry'" class="data-entry-stage">
          <h3>{{ $t('experiment.conduct.dataEntryTitle') }}</h3>
          <a-form
            ref="experimentDataFormRef"
            :model="experimentData"
            :label-col-props="{ span: 6 }"
            :wrapper-col-props="{ span: 18 }"
            label-align="left"
          >
            <a-row :gutter="16">
              <a-col :span="12">
                <a-form-item
                  :label="$t('experiment.form.label.ExperimentNo')"
                  field="ExperimentNo"
                  :rules="[
                    {
                      required: true,
                      message: $t(
                        'experiment.form.validation.ExperimentNoRequired'
                      ),
                    },
                  ]"
                >
                  <a-input
                    v-model="formDataExperimentNoComputed"
                    :placeholder="
                      $t('experiment.form.placeholder.ExperimentNo')
                    "
                  />
                </a-form-item>
              </a-col>
              <a-col :span="12">
                <a-form-item
                  :label="$t('experiment.form.label.MaterialCode')"
                  field="MaterialCode"
                  :rules="[
                    {
                      required: true,
                      message: $t(
                        'experiment.form.validation.MaterialCodeRequired'
                      ),
                    },
                  ]"
                >
                  <SearchSelect
                    v-model="materialCodeDataComputed"
                    :api-function="searchMaterials"
                    key-field="MaterialCode"
                    label-field="MaterialName"
                    :placeholder="
                      $t('experiment.form.placeholder.MaterialCode')
                    "
                  />
                </a-form-item>
              </a-col>
            </a-row>
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.ProtocolNo')"
                field="ProtocolNo"
                :rules="[
                  {
                    required: true,
                    message: $t(
                      'experiment.form.validation.ProtocolNoRequired'
                    ),
                  },
                ]"
              >
                <SearchSelect
                  v-model="protocolNoDataComputed"
                  :api-function="searchProtocols"
                  key-field="ProtocolNo"
                  label-field="ProtocolNo"
                  description-field="NSN"
                  :placeholder="$t('experiment.form.placeholder.ProtocolNo')"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.UserNo')"
                field="UserNo"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.UserNoRequired'),
                  },
                ]"
              >
                <SearchSelect
                  v-model="formDataUserNoComputed"
                  :api-function="searchUsers"
                  key-field="UserNo"
                  label-field="UserName"
                  :placeholder="$t('experiment.form.placeholder.UserNo')"
                />
              </a-form-item>
            </a-col>
          </a-form>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.HeatError')"
                field="HeatError"
                :rules="[
                  {
                    type: 'number',
                    message: $t('experiment.form.validation.HeatErrorNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="heatErrorDataComputed"
                  :step="0.01"
                  allow-clear
                  :placeholder="$t('experiment.form.placeholder.HeatError')"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.MixError')"
                field="MixError"
                :rules="[
                  {
                    type: 'number',
                    message: $t('experiment.form.validation.MixErrorNumber'),
                  },
                ]"
              >
                <a-input-number
                  v-model="mixErrorDataComputed"
                  :step="0.01"
                  allow-clear
                  :placeholder="$t('experiment.form.placeholder.MixError')"
                />
              </a-form-item>
            </a-col>
          </a-row>

          <a-row :gutter="16">
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.StartTime')"
                field="StartTime"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.StartTimeRequired'),
                  },
                ]"
              >
                <a-time-picker
                  v-model="startTimeDataComputed"
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                  allow-clear
                  :placeholder="$t('experiment.form.placeholder.StartTime')"
                />
              </a-form-item>
            </a-col>
            <a-col :span="12">
              <a-form-item
                :label="$t('experiment.form.label.EndTime')"
                field="EndTime"
                :rules="[
                  {
                    required: true,
                    message: $t('experiment.form.validation.EndTimeRequired'),
                  },
                ]"
              >
                <a-time-picker
                  v-model="endTimeDataComputed"
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                  allow-clear
                  :placeholder="$t('experiment.form.placeholder.EndTime')"
                />
              </a-form-item>
            </a-col>
          </a-row>
          <a-form-item
            :label="$t('experiment.form.label.GelTime')"
            field="GelTime"
          >
            <a-input v-model="gelTimeDataComputed" disabled />
          </a-form-item>

          <a-button
            type="primary"
            :loading="loading"
            class="upload-button"
            @click="uploadExperimentData"
          >
            {{ $t('experiment.conduct.uploadButton') }}
          </a-button>
        </div>
      </div>
    </a-card>
  </div>
</template>

<script lang="ts" setup>
  import { ref, reactive, computed, onMounted, nextTick } from 'vue';
  import { Message, FormInstance } from '@arco-design/web-vue';
  import useLoading from '@/hooks/loading';
  import { createExperiment, ExperimentRecord } from '@/api/experiment';
  import { useRouter } from 'vue-router';
  import { useI18n } from 'vue-i18n';
  import dayjs from 'dayjs';
  import duration from 'dayjs/plugin/duration';
  import staticImage1Url from '@/assets/images/63.png';
  import staticImage2Url from '@/assets/images/63FINAL.png';
  import experimentVideoUrl from '@/assets/images/expVideo.mp4';
  import experimentGifUrl from '@/assets/images/cat.gif';
  import SearchSelect from '@/components/searchSelect/index.vue';

  import { searchMaterials, type MaterialRecord } from '@/api/materials';
  import { searchProtocols, type ProtocolSearchRecord } from '@/api/protocol';
  import { searchUsers, type UserSearchRecord } from '@/api/userAdmin';

  dayjs.extend(duration);

  const router = useRouter();
  const { t } = useI18n();
  const { loading, setLoading } = useLoading();

  type Stage = 'prepare' | 'running' | 'data_entry' | 'finished';
  const currentStage = ref<Stage>('prepare');
  const loadingMedia = ref(false);

  const staticImage1 = ref(staticImage1Url); // 使用导入的 URL
  const staticImage2 = ref(staticImage2Url);
  const experimentVideo = ref(experimentVideoUrl);
  const experimentGif = ref(experimentGifUrl);
  const mediaType = ref<'video' | 'gif'>('video'); // 默认使用视频

  const videoPlayer = ref<HTMLVideoElement | null>(null);
  const experimentDataFormRef = ref<FormInstance | null>(null);

  // 实验数据模型
  const experimentData = reactive<{
    ExperimentNo: string;
    MaterialCode?: string | null;
    HeatError?: number | null;
    MixError?: number | null;
    StartTime?: string | null;
    EndTime?: string | null;
    ProtocolNo?: string | null;
    UserNo: string;
  }>({
    ExperimentNo: '',
    MaterialCode: undefined,
    HeatError: undefined,
    MixError: undefined,
    StartTime: undefined,
    EndTime: undefined,
    ProtocolNo: undefined,
    UserNo: '',
  });

  // 计算属性工厂，处理 number | null | undefined 类型 (用于 a-input-number)
  const createNumberComputed = (key: 'HeatError' | 'MixError') =>
    computed({
      get: () => {
        const value = experimentData[key];
        return value === null ? undefined : (value as number | undefined);
      },
      set: (value: number | undefined) => {
        (experimentData[key] as number | null | undefined) =
          value === undefined ? null : value;
      },
    });

  const heatErrorDataComputed = createNumberComputed('HeatError');
  const mixErrorDataComputed = createNumberComputed('MixError');

  // 计算属性工厂，处理 string | null | undefined 类型 (用于 a-input，包括必填字段)
  const createStringComputed = (
    key: 'ExperimentNo' | 'MaterialCode' | 'ProtocolNo' | 'UserNo'
  ) =>
    computed({
      get: () => {
        const value = experimentData[key];
        return value === null ? undefined : (value as string | undefined);
      },
      set: (value: string | undefined) => {
        (experimentData[key] as string | null | undefined) =
          value === undefined || value === '' ? null : value;
      },
    });

  const formDataExperimentNoComputed = createStringComputed('ExperimentNo');
  const materialCodeDataComputed = createStringComputed('MaterialCode');
  const protocolNoDataComputed = createStringComputed('ProtocolNo');
  const formDataUserNoComputed = createStringComputed('UserNo');

  // 计算属性工厂，用于 a-time-picker 的双向绑定，处理 null/undefined/'' 转换
  const createTimeComputed = (key: 'StartTime' | 'EndTime') =>
    computed({
      get: () => {
        const value = experimentData[key];
        return value === null ? undefined : (value as string | undefined);
      },
      set: (value: string | undefined) => {
        experimentData[key] =
          value === undefined || value === '' ? null : value;
      },
    });

  const startTimeDataComputed = createTimeComputed('StartTime');
  const endTimeDataComputed = createTimeComputed('EndTime');

  // GelTime 派生字段的计算属性 (保持不变，因为前端仍需显示)
  const gelTimeDataComputed = computed(() => {
    const start = experimentData.StartTime;
    const end = experimentData.EndTime;

    if (!start || !end) {
      return '';
    }
    console.log('Calculating GelTime for start:', start, 'end:', end);
    try {
      const dayjsStart = dayjs(`2000-01-01T${start}`);
      const dayjsEnd = dayjs(`2000-01-01T${end}`);

      let diff = dayjsEnd.diff(dayjsStart, 'second');

      if (diff < 0) {
        diff += 24 * 3600;
      }

      const durationObj = dayjs.duration(diff, 'seconds');
      const hours = String(durationObj.hours()).padStart(2, '0');
      const minutes = String(durationObj.minutes()).padStart(2, '0');
      const seconds = String(durationObj.seconds()).padStart(2, '0');

      return `${hours}:${minutes}:${seconds}`;
    } catch (e) {
      console.error('Error calculating GelTime:', e);
      return '计算错误';
    }
  });

  // 点击“开始实验”
  const startExperiment = () => {
    currentStage.value = 'running';
    loadingMedia.value = true;
    experimentData.StartTime = dayjs().format('HH:mm:ss');
    // experimentData.EndTime = null; // 重置结束时间
    // console.log(mediaType.value);
    // console.log(videoPlayer.value);
    if (mediaType.value === 'video') {
      nextTick(() => {
        // <-- 关键：等待 DOM 更新后才尝试访问 videoPlayer.value
        if (videoPlayer.value) {
          videoPlayer.value
            .play()
            .then(() => {
              loadingMedia.value = false;
            })
            .catch((error) => {
              Message.error(`视频播放失败: ${error.message || '未知错误'}`);
              loadingMedia.value = false;
              currentStage.value = 'prepare'; // 播放失败则回到准备阶段
            });
        } else {
          // 如果 after nextTick 仍然是 null，说明 ref 绑定失败或 DOM 渲染有问题
          Message.warning('视频播放器DOM元素未找到，无法播放。');
          loadingMedia.value = false;
          currentStage.value = 'prepare'; // 无法找到元素则回到准备阶段
        }
      });
    } else if (mediaType.value === 'gif') {
      loadingMedia.value = false;
    } else {
      // console.log("NONONO");
      loadingMedia.value = false;
      Message.warning('没有可播放的媒体文件。');
    }
  };

  // 媒体播放结束或GIF加载完成
  const onMediaEnded = () => {
    currentStage.value = 'data_entry';
    experimentData.EndTime = dayjs().format('HH:mm:ss');
    loadingMedia.value = false;
    Message.success('实验过程已完成，请填写数据。');
  };

  const onMediaLoaded = () => {
    // For GIF
    if (mediaType.value === 'gif') {
      Message.info(t('experiment.conduct.gifDelayMessage')); // 提示用户延迟
      setTimeout(() => {
        onMediaEnded(); // 10 秒后调用结束逻辑
      }, 10000);
    }
  };

  // 强制结束实验
  const endExperimentImmediately = () => {
    console.log('videoPlayer.value', videoPlayer.value);
    if (mediaType.value === 'video' && videoPlayer.value) {
      videoPlayer.value.pause();
      videoPlayer.value.currentTime = 0;
    }
    onMediaEnded();
  };

  // 上传实验数据
  const uploadExperimentData = async () => {
    const errors = await experimentDataFormRef.value?.validate();
    if (!errors) {
      setLoading(true);
      try {
        // 直接从 experimentData 中获取数据，因为计算属性的 setter 已经将其更新
        const dataToSend: Partial<ExperimentRecord> = {
          ExperimentNo: experimentData.ExperimentNo,
          MaterialCode: experimentData.MaterialCode,
          HeatError: experimentData.HeatError,
          MixError: experimentData.MixError,
          StartTime: experimentData.StartTime,
          EndTime: experimentData.EndTime,
          ProtocolNo: experimentData.ProtocolNo,
          UserNo: experimentData.UserNo,
        };

        // 统一处理可能为空的字段：将 undefined 或 '' 转换为 null
        // 由于计算属性的 setter 已经做了大部分工作，这里主要是确保最终数据的正确性
        const nullableStringFields: (keyof ExperimentRecord)[] = [
          'MaterialCode',
          'ProtocolNo',
        ];
        nullableStringFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        const nullableNumberFields: (keyof ExperimentRecord)[] = [
          'HeatError',
          'MixError',
        ];
        nullableNumberFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined || value === '') {
            (dataToSend as any)[key] = null;
          }
        });

        const nullableTimeFields: (keyof ExperimentRecord)[] = [
          'StartTime',
          'EndTime',
        ];
        nullableTimeFields.forEach((key) => {
          const value = dataToSend[key];
          if (value === undefined) {
            (dataToSend as any)[key] = null;
          }
        });

        // 如果ExperimentNo或UserNo是字符串且为空，也转换为null (虽然是required，但保险起见)
        if (dataToSend.ExperimentNo === '')
          dataToSend.ExperimentNo = null as any;
        if (dataToSend.UserNo === '') dataToSend.UserNo = null as any;

        await createExperiment(dataToSend as ExperimentRecord);
        Message.success(t('experiment.conduct.uploadSuccess'));
        router.push({ name: 'ExperimentAdminList' });
      } catch (error: any) {
        console.error('上传实验数据失败:', error);
        Message.error(
          `${t('experiment.conduct.uploadFail')}: ${
            error.message || '未知错误'
          }`
        );
      } finally {
        setLoading(false);
      }
    } else {
      Message.warning(t('groupForm.validationWarning'));
    }
  };

  onMounted(() => {
    // 可以在这里根据需要初始化 ExperimentNo 和 UserNo
    // 例如，从用户store获取当前登录用户的UserNo
    // import { useUserStore } from '@/store'; // 记得导入
    // const userStore = useUserStore();
    // if (userStore.userInfo.UserNo) {
    //     experimentData.UserNo = userStore.userInfo.UserNo;
    // }
    // 或者生成一个临时的 ExperimentNo
    // experimentData.ExperimentNo = 'EXP-' + dayjs().format('YYYYMMDDHHmmss');
  });
</script>

<script lang="ts">
  export default {
    name: 'ExperimentConduct',
  };
</script>

<style scoped lang="less">
  .container {
    padding: 0 20px 40px;
  }

  .general-card {
    display: flex;
    flex-direction: column;
    min-height: 400px;
  }

  .experiment-area {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    align-items: center;
    justify-content: center;
    padding: 20px;
    text-align: center;
    background-color: var(--color-fill-1);
    border: 1px dashed var(--color-border-2);
    border-radius: 4px;

    h3 {
      margin-bottom: 20px;
      color: var(--color-text-1);
    }
  }

  .preparation-stage,
  .running-stage,
  .data-entry-stage {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 800px;
  }

  .image-gallery {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-bottom: 30px;

    .experiment-image {
      width: 45%;
      max-width: 300px;
      height: auto;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgb(0 0 0 / 10%);
    }
  }

  .start-button {
    width: 200px;
    height: 50px;
    font-size: 18px;
  }

  .media-player {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 600px;
    min-height: 300px;
    margin-bottom: 20px;
    background-color: #000;

    .experiment-media {
      display: block;
      width: 100%;
      height: auto;
    }
  }

  .end-button {
    width: 180px;
    margin-top: 20px;
  }

  .data-entry-stage {
    .arco-form {
      width: 100%;
    }

    .upload-button {
      width: 200px;
      height: 50px;
      margin-top: 30px;
      font-size: 18px;
    }
  }

  .actions {
    position: sticky;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 100;
    height: 60px;
    padding: 14px 20px 14px 0;
    text-align: right;
    background: var(--color-bg-2);
    box-shadow: 0 -2px 8px rgb(0 0 0 / 10%);
    transform: translateY(100%);
    opacity: 0;
    transition: all 0.3s ease-in-out;
    pointer-events: none;
  }

  .data-entry-stage ~ .actions {
    transform: translateY(0%);
    opacity: 1;
    pointer-events: auto;
  }
</style>
