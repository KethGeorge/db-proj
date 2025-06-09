// src/api/modification.ts

import axios from 'axios';
import qs from 'query-string';

// 审计日志记录的结构 (与后端视图对应)
export interface ModificationRecord {
  ModificationID: string;
  OperationType: 'INSERT' | 'UPDATE' | 'DELETE';
  OperationTime: string; // 后端返回的 ISO 格式日期字符串
  OperatorUserNo: string; // 操作者的 UserNo
  OperatorUserName?: string | null; // 【新增】操作者的用户名
  EntityType: string;
  EntityID: string;
  FieldName?: string | null;
  OldValue?: string | null;
  NewValue?: string | null;
}

// 全局列表查询参数接口
export interface ModificationParams {
  current: number;
  pageSize: number;
  EntityType?: string;
  EntityID?: string;
  UserNo?: string; // 前端筛选时仍然叫 UserNo，后端API会做映射
  UserName?: string;
  OperationType?: 'INSERT' | 'UPDATE' | 'DELETE';
}

// 列表响应接口
export interface ModificationListRes {
  list: ModificationRecord[];
  total: number;
}

/**
 * @description 获取全局审计日志列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryModificationList(
  params: ModificationParams
): Promise<ModificationListRes> {
  return axios.get('/api/modification', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取指定用户的相关审计日志
 * @param userNo 要查询的用户的ID
 * @param params 分页参数
 */
export function queryModificationListByUser(
  userNo: string,
  params: { current: number; pageSize: number }
): Promise<ModificationListRes> {
  return axios.get(`/api/modification/by-user/${userNo}`, {
    params,
  });
}
