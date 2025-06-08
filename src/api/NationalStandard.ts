// frontend/src/api/national_standards.ts
import axios from 'axios'; // 确保这里导入的是您配置了响应拦截器（返回 res.data）的那个 axios 实例
import qs from 'query-string';

// National Standard Admin API 接口定义

// NationalStandardRecord 接口用于表示单个国家标准记录的结构
export interface NationalStandardRecord {
  NSN: string; // 国家标准号 (主键，唯一标识)
  StandardName: string; // 标准名称
  Description?: string; // 描述 (可选)
  MaterialCode?: string; // 材料代码 (可选)
}

// NationalStandardParams 接口用于查询列表时的参数
export interface NationalStandardParams
  extends Partial<NationalStandardRecord> {
  current: number;
  pageSize: number;
  // 额外的搜索参数，与国家标准表字段对应
  // NSN?: string; // 搜索时用的国家标准号
  // StandardName?: string; // 搜索时用的标准名称
  // Description?: string; // 搜索时用的描述
  // MaterialCode?: string; // 搜索时用的材料代码
}

// NationalStandardListRes 接口用于获取国家标准列表的响应数据结构
export interface NationalStandardListRes {
  list: NationalStandardRecord[];
  total: number;
}

export interface NationalStandardSearchRecord {
  NSN: string;
  StandardName: string; // StandardName 作为描述性字段
}

// --- API 函数定义 ---

/**
 * @description 获取国家标准列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryNationalStandardList(
  params: NationalStandardParams
): Promise<NationalStandardListRes> {
  return axios.get('/api/national_standards', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取单个国家标准详情
 * @param nsn 国家标准号
 */
export function queryNationalStandardDetail(
  nsn: string
): Promise<NationalStandardRecord> {
  return axios.get(`/api/national_standards/${nsn}`);
}

/**
 * @description 创建新国家标准
 * @param data 包含新国家标准信息的对象 (NSN, StandardName, Description, MaterialCode)
 */
export function createNationalStandard(
  data: NationalStandardRecord
): Promise<any> {
  // 注意：NSN 可能由后端生成，但前端在创建时也可能需要提供
  // 这里假设 NSN 在后端生成，前端只提供 StandardName, Description, MaterialCode
  // 如果前端需要提供 NSN，则将其添加到 data 中
  return axios.post('/api/national_standard', data);
}

/**
 * @description 更新国家标准信息
 * @param nsn 国家标准号
 * @param data 包含要更新字段的对象 (StandardName, Description, MaterialCode)
 */
export function updateNationalStandardInfo(
  nsn: string,
  data: Partial<NationalStandardRecord>
): Promise<any> {
  // 部分更新，只发送需要修改的字段
  return axios.put(`/api/national_standards/${nsn}`, data);
}

/**
 * @description 删除国家标准
 * @param nsn 国家标准号
 */
export function deleteNationalStandard(nsn: string): Promise<any> {
  return axios.delete(`/api/national_standards/${nsn}`);
}

export function searchNationalStandards(params: {
  query: string;
  limit?: number;
}): Promise<NationalStandardSearchRecord[]> {
  return axios.get('/api/national_standards/search', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
