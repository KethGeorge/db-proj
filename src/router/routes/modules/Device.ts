import { RouteRecordRaw } from 'vue-router';

// ... (其他导入) ...

// 导入新的设备管理组件 (注意导入路径中文件名已改为 device)
import DeviceList from '@/views/Device/deviceList.vue';
import DeviceForm from '@/views/Device/deviceForm.vue';

const deviceRoute: RouteRecordRaw[] = [
    {
        path: '/device-admin',
        name: 'DeviceAdmin',
        component: () => import('@/layout/default-layout.vue'),
        meta: {
            locale: 'menu.deviceAdmin',
            requiresAuth: true,
            icon: 'icon-desktop',
            order: 6,
            roles: ['admin', 'user'],
        },
        children: [
            {
                path: 'list',
                name: 'DeviceAdminList',
                component: DeviceList,
                meta: {
                    locale: 'menu.deviceAdmin.list',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: false,
                },
            },
            {
                path: 'create',
                name: 'DeviceAdminCreate',
                component: DeviceForm,
                meta: {
                    locale: 'menu.deviceAdmin.create',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'edit/:deviceNo',
                name: 'DeviceAdminEdit',
                component: DeviceForm,
                meta: {
                    locale: 'menu.deviceAdmin.edit',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'view/:deviceNo',
                name: 'DeviceAdminView',
                component: DeviceForm,
                meta: {
                    locale: 'menu.deviceAdmin.view',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: true,
                },
            },
        ]
    },
];

export default deviceRoute;
// 确保在你的主路由数组中导出 deviceRoute
// 例如：
// export default [
//   ...,
//   ...nationalStandardRoute,
//   ...materialRoute,
//   ...deviceRoute, // 添加新路由
// ];