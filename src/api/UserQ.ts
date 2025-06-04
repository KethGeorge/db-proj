// src/api/userQ.ts
import axios from 'axios';
import qs from 'query-string';

// User Admin API 接口定义
export interface UserRecord {
  id: string; // 对应 UserNo
  number: string; // 对应 UserNo (方便前端表格展示)
  name: string; // 对应 UserName
  userPermissions: string; // 对应 UserPermissions
  email: string; // 对应 Email
  telephone?: string; // 对应 Telephone，可以是可选的
  // 额外字段，可以根据后端实际返回或前端需要添加
  // password?: string; // 不应在前端直接显示，后端返回时用 '***'
}

export interface UserParams extends Partial<UserRecord> {
  current: number;
  pageSize: number;
  // 额外的搜索参数，与用户表字段对应
  userno?: string;
  username?: string;
  email?: string;
}

export interface UserListRes {
  list: UserRecord[];
  total: number;
}

// 用户列表查询 API
export function queryUserList(params: UserParams) {
  return axios.get<UserListRes>('/api/users', {
    params,
    paramsSerializer: (obj) => {
      return qs.stringify(obj);
    },
  });
}