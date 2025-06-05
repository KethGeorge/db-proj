import { RouteRecordRaw } from 'vue-router';

// ... (其他导入，例如 NationalStandardFormPage, NationalStandardTable) ...

// 导入新的材料管理组件
import MaterialList from '@/views/material/materialsList.vue'; // 假设你有一个材料列表组件
import MaterialForm from '@/views/material/materialsForm.vue'; // 假设你有一个材料表单组件

const materialRoute: RouteRecordRaw[] = [
    {
        path: '/material-admin', // 定义材料管理页面的父级路径
        name: 'MaterialAdmin', // 父级路由名称
        component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
        meta: {
            locale: 'menu.materialAdmin', // 侧边栏菜单的国际化 key
            requiresAuth: true,
            icon: 'icon-apps', // 示例图标 (Arco Design 的应用图标)
            order: 5, // 在侧边栏菜单中的排序，紧随国家标准管理之后
            roles: ['admin', 'user'], // 示例：管理员和普通用户都可以访问这个模块
        },
        children: [
            {
                path: 'list', // 完整路径 /material-admin/list
                name: 'MaterialAdminList', // 材料列表页面的路由名称
                component: MaterialList,
                meta: {
                    locale: 'menu.materialAdmin.list',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: false,
                },
            },
            {
                path: 'create', // 完整路径 /material-admin/create
                name: 'MaterialAdminCreate', // 创建材料表单页面的路由名称
                component: MaterialForm,
                meta: {
                    locale: 'menu.materialAdmin.create',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'edit/:materialCode', // 动态路由参数，例如 /material-admin/edit/MAT-001
                name: 'MaterialAdminEdit',
                component: MaterialForm, // 与创建页面复用同一个表单组件
                meta: {
                    locale: 'menu.materialAdmin.edit',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'view/:materialCode', // 动态路由参数，例如 /material-admin/view/MAT-001
                name: 'MaterialAdminView',
                component: MaterialForm, // 与创建/编辑页面复用同一个表单组件
                meta: {
                    locale: 'menu.materialAdmin.view',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: true,
                },
            },
        ]
    },
];

export default materialRoute;
// 确保在你的主路由数组中导出 materialRoute
// 例如：
// export default [
//   ..., // 其他路由
//   ...nationalStandardRoute,
//   ...materialRoute, // 添加新路由
// ];