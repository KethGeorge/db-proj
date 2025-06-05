// src/api/userQ.ts
import axios from 'axios'; // 确保这里导入的是您配置了响应拦截器（返回 res.data）的那个 axios 实例
import qs from 'query-string';

// User Admin API 接口定义

// UserRecord 接口现在也用于发送数据（如创建和更新），
// 因此 password 字段应包含在这里，以便前端能够构建请求体。
export interface UserRecord {
  id?: string; // 对应 UserNo，后端返回时有，前端创建/更新时不一定需要发送
  number?: string; // 对应 UserNo (方便前端表格展示)，后端返回时有
  username: string; // 对应 UserName
  password?: string; // 对应 UserPassword，创建时必填，更新时可选（或通过专门接口）
  userPermissions: string; // 对应 UserPermissions
  email: string; // 对应 Email
  telephone?: string; // 对应 Telephone，可以是可选的
  // 额外字段，可以根据后端实际返回或前端需要添加
}

export interface UserParams extends Partial<UserRecord> {
  current: number;
  pageSize: number;
  // 额外的搜索参数，与用户表字段对应
  userno?: string; // 搜索时用的用户编号
  username?: string; // 搜索时用的用户名
  email?: string; // 搜索时用的邮箱
}

export interface UserListRes {
  list: UserRecord[];
  total: number;
}

// 后端统一返回结构（通常由 Axios 拦截器处理，这里为了明确类型，
// 但在 api 文件中不再直接使用它作为函数返回类型，因为拦截器会剥离它）
// interface HttpResponse<T = any> {
//   code: number;
//   message: string;
//   data: T;
// }

// --- API 函数定义 ---

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
 * @param userno 用户编号
 */
export function queryUserDetail(userno: string): Promise<UserRecord> {
  // 后端返回的是单个 UserRecord，且不包含明文密码
  return axios.get(`/api/users/${userno}`);
}

/**
 * @description 创建新用户
 * @param data 包含新用户信息的对象 (username, password, email, userPermissions, telephone)
 */
export function createUser(data: UserRecord): Promise<any> { // 返回 any 或 void，取决于后端创建成功后是否有特定返回数据
  // 后端 /api/user 接收的字段
  return axios.post('/api/user', data);
}

/**
 * @description 更新用户信息 (不包括密码)
 * @param userno 用户编号
 * @param data 包含要更新字段的对象 (username, email, telephone, userPermissions, password)
 */
export function updateUserInfo(userno: string, data: Partial<UserRecord>): Promise<any> { // 返回 any 或 void
  // 部分更新，只发送需要修改的字段
  // 注意：此处后端 /api/users/<userno> 会处理 password 字段，如果传入则更新
  return axios.put(`/api/users/${userno}`, data);
}

/**
 * @description 更新用户密码
 * @param userno 用户编号
 * @param newPassword 新密码（明文）
 * @param currentPassword 当前密码（明文，如果后端需要验证旧密码）
 */
export function updateUserPassword(userno: string, newPassword: string, currentPassword?: string): Promise<any> { // 返回 any 或 void
  const payload: { new_password: string; current_password?: string } = {
    new_password: newPassword,
  };
  if (currentPassword) {
    payload.current_password = currentPassword;
  }
  // 专门的密码修改接口
  return axios.put(`/api/users/${userno}/password`, payload);
}