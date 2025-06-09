// src/router/routes/modules/modification.ts
import { RouteRecordRaw } from 'vue-router';
import { DEFAULT_LAYOUT } from '../base';

const MODIFICATION: RouteRecordRaw = {
  path: '/audit',
  name: 'audit',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.audit',
    requiresAuth: true,
    icon: 'icon-history', // 历史/记录图标
    order: 9, // 调整在菜单中的顺序
    roles: ['admin'], // 只有管理员可以查看
  },
  children: [
    {
      path: 'log',
      name: 'AuditLog',
      component: () => import('@/views/modification/modificationList.vue'),
      meta: {
        locale: 'menu.audit.log',
        requiresAuth: true,
        roles: ['admin'],
      },
    },
  ],
};

export default MODIFICATION;
