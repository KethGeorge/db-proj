// frontend/src/api/experiment.ts
import axios from 'axios';
import qs from 'query-string';

// ExperimentRecord 接口用于表示单个实验记录的结构
// 移除 GelTime 字段
export interface ExperimentRecord {
  ExperimentNo: string;
  MaterialCode?: string | null;
  HeatError?: number | null;
  MixError?: number | null;
  StartTime?: string | null; // TIME 类型在前端用字符串 (HH:MM:SS)
  EndTime?: string | null;
  // GelTime?: string | null; // <-- 移除此行
  ProtocolNo?: string | null;
  UserNo: string; // 实验本身的UserNo
}

// ExperimentParams 和 ExperimentListRes 保持不变
export interface ExperimentParams extends Partial<ExperimentRecord> {
  current: number;
  pageSize: number;
}

export interface ExperimentListRes {
  list: ExperimentRecord[];
  total: number;
}

// API 函数定义 (保持不变，因为 GelTime 不在请求体中传递)
/**
 * @description 获取实验列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryExperimentList(params: ExperimentParams): Promise<ExperimentListRes> {
  return axios.get('/api/experiment', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取单个实验详情
 * @param experimentNo 实验编号
 */
export function queryExperimentDetail(experimentNo: string): Promise<ExperimentRecord> {
  return axios.get(`/api/experiment/${experimentNo}`);
}

/**
 * @description 创建新实验
 * @param data 包含新实验信息的对象
 */
export function createExperiment(data: ExperimentRecord): Promise<any> {
  return axios.post('/api/experiment', data);
}

/**
 * @description 更新实验信息
 * @param experimentNo 实验编号
 * @param data 包含要更新字段的对象
 */
export function updateExperimentInfo(experimentNo: string, data: Partial<ExperimentRecord>): Promise<any> {
  return axios.put(`/api/experiment/${experimentNo}`, data);
}

/**
 * @description 删除实验
 * @param experimentNo 实验编号
 */
export function deleteExperiment(experimentNo: string): Promise<any> {
  return axios.delete(`/api/experiment/${experimentNo}`);
}