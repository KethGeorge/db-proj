import { RouteRecordRaw } from 'vue-router';

// 导入你的 NationalStandard 组件
// 根据您的文件结构，它可能位于 views/NationalStandard/index.vue
// 确保路径正确
import NationalStandardIndex from '@/views/NationalStandard/index.vue';

const nationalStandardRoute: RouteRecordRaw[] = [
    {
        path: '/national-standard', // 定义国标页面的父级路径
        name: 'nationalStandard', // 父级路由名称 (可选)
        component: () => import('@/layout/default-layout.vue'), // 如果有布局组件，通常在这里引入
        meta: {
            locale: 'menu.nationalStandard', // 侧边栏菜单的国际化 key (对应 src/locale 目录下的文件)，需要您在语言文件中添加 'menu.nationalStandard'
            requiresAuth: true, // 是否需要登录权限
            icon: 'icon-file', // 侧边栏菜单图标 (对应 Arco Design 图标库)，这里用了一个示例图标
            order: 4, // 在侧边栏菜单中的排序 (数字越小越靠前)，请根据您的需求调整
        },
        children: [
            {
                path: '', // 子路径为空，表示主页面，完整路径会是 /national-standard
                name: 'nationalStandardIndex', // 页面路由名称
                component: NationalStandardIndex, // 页面组件，即 views/NationalStandard/index.vue
                meta: {
                    locale: 'menu.nationalStandard.index', // 页面在侧边栏或面包屑中的国际化 key，需要您在语言文件中添加 'menu.nationalStandard.index'
                    requiresAuth: true,
                    roles: ['admin', 'user'], // 可选：指定哪些角色可以访问，请根据您的权限设计调整
                },
            },
        ],
    },
];

export default nationalStandardRoute;