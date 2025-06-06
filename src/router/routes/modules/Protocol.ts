import { RouteRecordRaw } from 'vue-router';

// ... (其他导入) ...

// 导入新的协议管理组件
import ProtocolList from '@/views/protocol/protocolList.vue';
import ProtocolForm from '@/views/protocol/protocolForm.vue';

const protocolRoute: RouteRecordRaw[] = [
    {
        path: '/protocol-admin', // 定义协议管理页面的父级路径
        name: 'ProtocolAdmin', // 父级路由名称
        component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
        meta: {
            locale: 'menu.protocolAdmin', // 侧边栏菜单的国际化 key
            requiresAuth: true,
            icon: 'icon-align-left', // 示例图标 (Arco Design 的对齐图标)
            order: 7, // 在侧边栏菜单中的排序
            roles: ['admin', 'user'], // 示例：管理员和普通用户都可以访问这个模块
        },
        children: [
            {
                path: 'list', // 完整路径 /protocol-admin/list
                name: 'ProtocolAdminList', // 协议列表页面的路由名称
                component: ProtocolList,
                meta: {
                    locale: 'menu.protocolAdmin.list',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: false,
                },
            },
            {
                path: 'create', // 完整路径 /protocol-admin/create
                name: 'ProtocolAdminCreate', // 创建协议表单页面的路由名称
                component: ProtocolForm,
                meta: {
                    locale: 'menu.protocolAdmin.create',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'edit/:protocolNo', // 动态路由参数
                name: 'ProtocolAdminEdit',
                component: ProtocolForm, // 与创建页面复用同一个表单组件
                meta: {
                    locale: 'menu.protocolAdmin.edit',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'view/:protocolNo', // 动态路由参数
                name: 'ProtocolAdminView',
                component: ProtocolForm, // 与创建/编辑页面复用同一个表单组件
                meta: {
                    locale: 'menu.protocolAdmin.view',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: true,
                },
            },
        ]
    },
];

// 确保在你的主路由数组中导出 protocolRoute
// 例如：
// export default [
//   ..., // 其他路由
//   ...nationalStandardRoute,
//   ...materialRoute,
//   ...deviceRoute,
//   ...protocolRoute, // 添加新路由
// ];
export default protocolRoute;