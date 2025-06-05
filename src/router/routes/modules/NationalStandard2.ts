import { RouteRecordRaw } from 'vue-router';

// 导入你的国家标准管理组件
import NationalStandardFormPage from '@/views/NS2/NSForm.vue'; // 假设你有一个国家标准表单组件
import NationalStandardTable from '@/views/NS2/NSList.vue'; // 假设你有一个国家标准列表组件

const nationalStandardRoute: RouteRecordRaw[] = [
    {
        path: '/national-standard-admin', // 定义国家标准管理页面的父级路径
        name: 'NationalStandardAdmin', // 父级路由名称
        component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
        meta: {
            locale: 'menu.nationalStandardAdmin', // 侧边栏菜单的国际化 key
            requiresAuth: true,
            icon: 'icon-file', // 示例图标 (Arco Design 的标签图标)
            order: 4, // 在侧边栏菜单中的排序
            roles: ['admin', 'user'], // 示例：管理员和普通用户都可以访问这个模块
        },
        children: [
            {
                path: 'list', // 完整路径 /national-standard-admin/list
                name: 'NationalStandardAdminList', // 国家标准列表页面的路由名称
                component: NationalStandardTable,
                meta: {
                    locale: 'menu.nationalStandardAdmin.list', // 国际化 key
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: false, // 列表页通常不隐藏
                },
            },
            {
                path: 'create', // 完整路径 /national-standard-admin/create
                name: 'NationalStandardAdminCreate', // 创建国家标准表单页面的路由名称
                component: NationalStandardFormPage,
                meta: {
                    locale: 'menu.nationalStandardAdmin.create',
                    requiresAuth: true,
                    roles: ['admin'], // 通常只有管理员角色可以创建
                    hideInMenu: true, // 创建页面通常不在菜单中显示
                },
            },
            {
                path: 'edit/:nsn', // 动态路由参数，例如 /national-standard-admin/edit/GB-T123
                name: 'NationalStandardAdminEdit',
                component: NationalStandardFormPage, // 与创建页面复用同一个表单组件
                meta: {
                    locale: 'menu.nationalStandardAdmin.edit',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true, // 编辑页面通常不在菜单中显示
                },
            },
            {
                path: 'view/:nsn', // 动态路由参数，例如 /national-standard-admin/view/GB-T123
                name: 'NationalStandardAdminView',
                component: NationalStandardFormPage, // 与创建/编辑页面复用同一个表单组件
                meta: {
                    locale: 'menu.nationalStandardAdmin.view',
                    requiresAuth: true,
                    roles: ['admin', 'user'], // 普通用户也可以查看详情
                    hideInMenu: true, // 详情页面通常不在菜单中显示
                },
            },
        ]
    },
];

export default nationalStandardRoute;