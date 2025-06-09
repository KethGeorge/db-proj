// src/api/report.ts

import axios from 'axios';
import qs from 'query-string';

// 主报告详情
export interface ReportDetailsRecord {
  ExperimentCode: string;
  ExperimentNo: string;
  ExperimentName: string | null;
  ExperimentalStatus: string | null;
}

// HEC 子报告
export interface HECRecord {
  HEC: string;
  Temperature: number | null;
  Time1: string | null; // TIME in backend is string 'HH:MM:SS'
  SafeArea: number | null;
  ExperimentCode: string;
}

// MEC 子报告
export interface MECRecord {
  MEC: string;
  HeightError: number | null;
  PlainError: number | null;
  ErrorArea: number | null;
  SpeedError: number | null;
  Time2: string | null;
  ExperimentCode: string;
}

// MTEC 子报告
export interface MTECRecord {
  MTEC: string;
  PhotoPath: string | null;
  IsGel: boolean | null;
  Time3: string | null;
  ExperimentCode: string;
}

// 完整的实验报告数据结构
export interface ExperimentReportRecord {
  reportDetails: ReportDetailsRecord;
  hecData: HECRecord | null;
  mecData: MECRecord | null;
  mtecData: MTECRecord | null;
}

export type ReportListItem = ReportDetailsRecord;

export interface ReportListParams extends Partial<ReportListItem> {
  current: number;
  pageSize: number;
}

// 列表响应
export interface ReportListRes {
  list: ReportListItem[];
  total: number;
}

// --- 新增：获取报告列表的 API 函数 ---
export function queryReportList(
  params: ReportListParams
): Promise<ReportListRes> {
  return axios.get('/api/reports', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 根据实验编号获取完整的实验报告
 * @param experimentNo 实验编号
 */
export function queryExperimentReport(
  experimentNo: string
): Promise<ExperimentReportRecord> {
  return axios.get(`/api/report/${experimentNo}`);
}
