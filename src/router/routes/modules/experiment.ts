import { RouteRecordRaw } from 'vue-router';

// ... (其他导入) ...

// 导入新的实验管理组件
import ExperimentList from '@/views/experiment/experimentList.vue';
import ExperimentForm from '@/views/experiment/experimentForm.vue';
// 导入实验操作界面
import ExperimentConduct from '@/views/experiment/experimentConduct.vue'; // 新增的实验操作页面

const experimentRoute: RouteRecordRaw[] = [
    {
        path: '/experiment-admin', // 定义实验管理页面的父级路径
        name: 'ExperimentAdmin', // 父级路由名称
        component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
        meta: {
            locale: 'menu.experimentAdmin', // 侧边栏菜单的国际化 key
            requiresAuth: true,
            icon: 'icon-robot', // 示例图标 (Arco Design 的机器人图标)
            order: 8, // 在侧边栏菜单中的排序
            roles: ['admin', 'user'], // 示例：管理员和普通用户都可以访问这个模块
        },
        children: [
            {
                path: 'list', // 完整路径 /experiment-admin/list
                name: 'ExperimentAdminList', // 实验列表页面的路由名称
                component: ExperimentList,
                meta: {
                    locale: 'menu.experimentAdmin.list',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: false,
                },
            },
            {
                path: 'create', // 完整路径 /experiment-admin/create
                name: 'ExperimentAdminCreate', // 创建实验表单页面的路由名称
                component: ExperimentForm,
                meta: {
                    locale: 'menu.experimentAdmin.create',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'edit/:experimentNo', // 动态路由参数
                name: 'ExperimentAdminEdit',
                component: ExperimentForm, // 与创建页面复用同一个表单组件
                meta: {
                    locale: 'menu.experimentAdmin.edit',
                    requiresAuth: true,
                    roles: ['admin'],
                    hideInMenu: true,
                },
            },
            {
                path: 'view/:experimentNo', // 动态路由参数
                name: 'ExperimentAdminView',
                component: ExperimentForm, // 与创建/编辑页面复用同一个表单组件
                meta: {
                    locale: 'menu.experimentAdmin.view',
                    requiresAuth: true,
                    roles: ['admin', 'user'],
                    hideInMenu: true,
                },
            },
            // 新增的实验操作页面路由
            {
                path: 'conduct', // 完整路径 /experiment-admin/conduct
                name: 'ExperimentAdminConduct',
                component: ExperimentConduct,
                meta: {
                    locale: 'menu.experimentAdmin.conduct', // 例如：执行实验
                    requiresAuth: true,
                    roles: ['user', 'admin'], // 假设普通用户可以执行实验
                    hideInMenu: false, // 可以在菜单中显示
                },
            },
        ]
    },
];

export default experimentRoute;
// 确保在你的主路由数组中导出 experimentRoute
// 例如：
// export default [
//   ..., // 其他路由
//   ...nationalStandardRoute,
//   ...materialRoute,
//   ...deviceRoute,
//   ...protocolRoute,
//   ...experimentRoute, // 添加新路由
// ];