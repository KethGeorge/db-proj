import axios from 'axios';
import type { RouteRecordNormalized } from 'vue-router';
import { UserState } from '@/store/modules/user/types';

export interface LoginData {
  username: string;
  password: string;
}

export interface LoginRes {
  token: string;
}
export function login(data: LoginData): Promise<LoginRes> {
  return axios.post('/api/user/login', data);
}

// logout 函数返回的 Promise 可能没有特定的数据，或者返回一个通用成功消息
export function logout(): Promise<any> { // 或者 Promise<void> 如果没有返回数据
  return axios.post('/api/user/logout');
}

// 确保 getUserInfo 函数返回的 Promise 直接解析为 UserState 类型
export function getUserInfo(): Promise<UserState> { // 或者 Promise<UserInfoData> 如果定义了
  return axios.post('/api/user/info'); // 这里不再需要泛型，因为它由拦截器处理
}

// 确保 getMenuList 函数返回的 Promise 直接解析为 RouteRecordNormalized[] 类型
export function getMenuList(): Promise<RouteRecordNormalized[]> {
  return axios.post('/api/user/menu');
}
