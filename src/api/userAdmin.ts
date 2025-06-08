import axios from 'axios';
import qs from 'query-string';

export interface UserRecord {
  UserNo?: string;
  UserName: string;
  UserPassword?: string;
  UserPermissions?: string | null;
  Email?: string | null;
  Telephone?: string | null;
}

export interface UserParams extends Partial<UserRecord> {
  current: number;
  pageSize: number;
}

export interface UserListRes {
  list: UserRecord[];
  total: number;
}
export interface UserSearchRecord {
  UserNo: string;
  UserName: string;
}

/**
 * @description 获取用户列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryUserList(params: UserParams): Promise<UserListRes> {
  return axios.get('/api/users', {
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
  return axios.get(`/api/users/${userno}`);
}

/**
 * @description 创建新用户
 * @param data 包含新用户信息的对象
 */
export function createUser(data: UserRecord): Promise<any> {
  return axios.post('/api/user', data);
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
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}
