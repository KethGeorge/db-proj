// frontend/src/api/user.ts

import axios from 'axios';
import qs from 'query-string';

// UserRecord 接口定义：严格匹配后端 users 表的字段名和类型
export interface UserRecord {
  UserNo?: string; // CHAR(8), 对于创建操作，UserNo可能由后端生成；对于查询和更新，它会存在
  UserName: string; // CHAR(20)
  UserPassword?: string; // CHAR(20)，创建时必填，更新时可选
  UserPermissions?: string | null; // CHAR(5)
  Email?: string | null; // VARCHAR(20)
  Telephone?: string | null; // CHAR(13)
  // 其他可能的字段，如 Avatar, Job, Organization, Location, Certification，如果后端返回也应在此处定义
}

// UserParams 接口：用于用户列表查询的参数
export interface UserParams extends Partial<UserRecord> {
  current: number;
  pageSize: number;
  // 搜索参数直接使用 UserRecord 字段
}

// UserListRes 接口：用户列表返回结果
export interface UserListRes {
  list: UserRecord[];
  total: number;
}

// UserSearchRecord 接口：用于搜索选择器，只包含 UserNo 和 UserName
export interface UserSearchRecord {
  UserNo: string;
  UserName: string;
}

// --- API 函数定义 ---

/**
 * @description 获取用户列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryUserList(params: UserParams): Promise<UserListRes> {
  return axios.get('/api/users', {
    // 注意是 /api/users (复数)
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}

/**
 * @description 获取单个用户详情
 * @param userno 用户编号 (UserNo)
 */
export function queryUserDetail(userno: string): Promise<UserRecord> {
  return axios.get(`/api/users/${userno}`); // 注意是 /api/users/{userno}
}

/**
 * @description 创建新用户
 * @param data 包含新用户信息的对象
 */
export function createUser(data: UserRecord): Promise<any> {
  return axios.post('/api/user', data); // 注意是 /api/user (单数)
}

/**
 * @description 更新用户信息
 * @param userno 用户编号 (UserNo)
 * @param data 包含要更新字段的对象
 */
export function updateUserInfo(
  userno: string,
  data: Partial<UserRecord>
): Promise<any> {
  return axios.put(`/api/users/${userno}`, data);
}

/**
 * @description 更新用户密码
 * @param userno 用户编号 (UserNo)
 * @param newPassword 新密码
 * @param currentPassword 当前密码 (如果后端需要)
 */
export function updateUserPassword(
  userno: string,
  newPassword: string,
  currentPassword?: string
): Promise<any> {
  const payload: { new_password: string; current_password?: string } = {
    new_password: newPassword,
  };
  if (currentPassword) {
    payload.current_password = currentPassword;
  }
  return axios.put(`/api/users/${userno}/password`, payload);
}

/**
 * @description 删除用户
 * @param userno 用户编号 (UserNo)
 */
export function deleteUser(userno: string): Promise<any> {
  return axios.delete(`/api/users/${userno}`);
}

/**
 * @description 搜索用户，用于外键选择器
 * @param params 搜索参数 (query, limit)
 */
export function searchUsers(params: {
  query: string;
  limit?: number;
}): Promise<UserSearchRecord[]> {
  return axios.get('/api/users/search', {
    // 注意是 /api/users/search (复数)
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
