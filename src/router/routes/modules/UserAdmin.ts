import { RouteRecordRaw } from 'vue-router';

import UserList from '@/views/userAdmin/userAdminList.vue';
import UserForm from '@/views/userAdmin/userAdminForm.vue';

const userAdminRoute: RouteRecordRaw[] = [
  {
    path: '/user-admin',
    name: 'UserAdmin',
    component: () => import('@/layout/default-layout.vue'),
    meta: {
      locale: 'menu.userAdmin',
      requiresAuth: true,
      icon: 'icon-user',
      order: 4,
      roles: ['admin'],
    },
    children: [
      {
        path: 'list', // 完整路径 /user-admin/list
        name: 'UserAdminList', // 用户列表页面的路由名称
        component: UserList, // <-- 指向新的用户列表组件
        meta: {
          locale: 'menu.userAdmin.list',
          requiresAuth: true,
          roles: ['admin'],
          hideInMenu: false,
        },
      },
      {
        path: 'create', // 完整路径 /user-admin/create
        name: 'UserAdminCreate', // 创建用户表单页面的路由名称
        component: UserForm, // <-- 指向新的用户表单组件
        meta: {
          locale: 'menu.userAdmin.create',
          requiresAuth: true,
          roles: ['admin'],
          hideInMenu: true,
        },
      },
      {
        path: 'edit/:userno', // 动态路由参数
        name: 'UserAdminEdit',
        component: UserForm, // <-- 指向新的用户表单组件
        meta: {
          locale: 'menu.userAdmin.edit',
          requiresAuth: true,
          roles: ['admin'],
          hideInMenu: true,
        },
      },
      {
        path: 'view/:userno', // 动态路由参数
        name: 'UserAdminView',
        component: UserForm, // <-- 指向新的用户表单组件
        meta: {
          locale: 'menu.userAdmin.view',
          requiresAuth: true,
          roles: ['admin', 'user'], // 通常普通用户也可以查看自己的详情
          hideInMenu: true,
        },
      },
    ],
  },
];

export default userAdminRoute;
// ... (其他路由模块的导出，例如 nationalStandardRoute, materialRoute, deviceRoute, protocolRoute, experimentRoute) ...
// 确保在你的主路由数组中导出 userAdminRoute
// 示例：
// export default [
//   ...,
//   ...userAdminRoute, // <-- 添加新的用户管理路由
//   ...nationalStandardRoute,
//   ...materialRoute,
//   ...deviceRoute,
//   ...protocolRoute,
//   ...experimentRoute,
// ];
