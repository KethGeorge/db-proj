// frontend/src/api/protocol.ts
import axios from 'axios';
import qs from 'query-string';

// ProtocolRecord 接口用于表示单个协议记录的结构
// 所有字段都可能为可选，因为在更新时只传部分字段
export interface ProtocolRecord {
  ProtocolNo: string;
  NSN?: string;
  SHT?: number | null; // 浮点数，可能为 null
  SMS?: number | null;
  MixingAngle?: number | null;
  MixingRadius?: number | null;
  MeasurementInterval?: number | null;
  MaterialCode: string; // 外码，必填
  UserNo: string; // 外码，必填
}

// ProtocolParams 接口用于查询列表时的参数
export interface ProtocolParams extends Partial<ProtocolRecord> {
  current: number;
  pageSize: number;
}

// ProtocolListRes 接口用于获取协议列表的响应数据结构
export interface ProtocolListRes {
  list: ProtocolRecord[];
  total: number;
}

// --- API 函数定义 ---

/**
 * @description 获取协议列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryProtocolList(
  params: ProtocolParams
): Promise<ProtocolListRes> {
  return axios.get('/api/protocol', {
    // <-- 路径为 /api/protocol
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取单个协议详情
 * @param protocolNo 协议编码
 */
export function queryProtocolDetail(
  protocolNo: string
): Promise<ProtocolRecord> {
  return axios.get(`/api/protocol/${protocolNo}`); // <-- 路径为 /api/protocol/{id}
}

/**
 * @description 创建新协议
 * @param data 包含新协议信息的对象
 */
export function createProtocol(data: ProtocolRecord): Promise<any> {
  return axios.post('/api/protocol', data); // <-- 路径为 /api/protocol (POST)
}

/**
 * @description 更新协议信息
 * @param protocolNo 协议编码
 * @param data 包含要更新字段的对象
 */
export function updateProtocolInfo(
  protocolNo: string,
  data: Partial<ProtocolRecord>
): Promise<any> {
  return axios.put(`/api/protocol/${protocolNo}`, data); // <-- 路径为 /api/protocol/{id}
}

/**
 * @description 删除协议
 * @param protocolNo 协议编码
 */
export function deleteProtocol(protocolNo: string): Promise<any> {
  return axios.delete(`/api/protocol/${protocolNo}`); // <-- 路径为 /api/protocol/{id}
}

export interface ProtocolSearchRecord {
  ProtocolNo: string;
  NSN?: string | null; // NSN 作为描述性字段
}

/**
 * @description 搜索协议，用于外键选择器
 * @param params 搜索参数 (query, limit)
 */
export function searchProtocols(params: {
  query: string;
  limit?: number;
}): Promise<ProtocolSearchRecord[]> {
  return axios.get('/api/protocols/search', {
    // 注意是 /api/protocols/search (复数)
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
