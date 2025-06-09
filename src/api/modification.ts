// src/api/modification.ts
import axios from 'axios';
import qs from 'query-string';

// 审计日志记录的结构
export interface ModificationRecord {
  ModificationID: string;
  OperationType: 'INSERT' | 'UPDATE' | 'DELETE';
  OperationTime: string; // 后端返回的 ISO 格式日期字符串
  UserNo: string;
  EntityType: string;
  EntityID: string;
  FieldName?: string | null;
  OldValue?: string | null;
  NewValue?: string | null;
}

// 查询参数接口
export interface ModificationParams
  extends Partial<
    Omit<ModificationRecord, 'ModificationID' | 'OperationTime'>
  > {
  current: number;
  pageSize: number;
}

// 列表响应接口
export interface ModificationListRes {
  list: ModificationRecord[];
  total: number;
}

/**
 * @description 获取审计日志列表
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
