// frontend/src/api/materials.ts
import axios from 'axios';
import qs from 'query-string';

// MaterialRecord 接口用于表示单个材料记录的结构
export interface MaterialRecord {
  MaterialCode: string; // 材料编码 (主键，必填)
  MaterialName: string; // 材料名称 (必填)
}

// MaterialParams 接口用于查询列表时的参数
export interface MaterialParams extends Partial<MaterialRecord> {
  current: number;
  pageSize: number;
}

// MaterialListRes 接口用于获取材料列表的响应数据结构
export interface MaterialListRes {
  list: MaterialRecord[];
  total: number;
}

// --- API 函数定义 ---

/**
 * @description 获取材料列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryMaterialList(params: MaterialParams): Promise<MaterialListRes> {
  return axios.get('/api/materials', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取单个材料详情
 * @param materialCode 材料编码
 */
export function queryMaterialDetail(materialCode: string): Promise<MaterialRecord> {
  return axios.get(`/api/materials/${materialCode}`);
}

/**
 * @description 创建新材料
 * @param data 包含新材料信息的对象 (MaterialCode, MaterialName)
 */
export function createMaterial(data: MaterialRecord): Promise<any> {
  return axios.post('/api/material', data);
}

/**
 * @description 更新材料信息
 * @param materialCode 材料编码
 * @param data 包含要更新字段的对象 (MaterialName)
 */
export function updateMaterialInfo(materialCode: string, data: Partial<MaterialRecord>): Promise<any> {
  return axios.put(`/api/materials/${materialCode}`, data);
}

/**
 * @description 删除材料
 * @param materialCode 材料编码
 */
export function deleteMaterial(materialCode: string): Promise<any> {
  return axios.delete(`/api/materials/${materialCode}`);
}