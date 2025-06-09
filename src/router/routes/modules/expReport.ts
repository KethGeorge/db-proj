// src/router/modules/report.ts

import { RouteRecordRaw } from 'vue-router';
import { DEFAULT_LAYOUT } from '../base';

const REPORT: RouteRecordRaw = {
  path: '/experiment-report',
  name: 'ExperimentReport',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.report',
    requiresAuth: true,
    icon: 'icon-nav', // 报告图标
    order: 9, // 调整菜单顺序
  },
  children: [
    {
      path: 'list',
      name: 'ExperimentReportList',
      component: () => import('@/views/expReport/expReportList.vue'), // 新的列表页
      meta: {
        locale: 'menu.report.list',
        requiresAuth: true,
        roles: ['admin', 'user'],
      },
    },
    {
      path: 'view/:experimentNo', // 路由参数仍为 experimentNo
      name: 'ExperimentReportView', // 路由名修改以区分
      component: () => import('@/views/expReport/expReportForm.vue'), // 详情页
      meta: {
        locale: 'menu.report.view',
        requiresAuth: true,
        roles: ['admin', 'user'],
        hideInMenu: true, // 在菜单中隐藏详情页
      },
    },
  ],
};

export default REPORT;
