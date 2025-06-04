import { RouteRecordRaw } from 'vue-router';

// 导入你的用户管理表单组件
// 根据我们之前讨论的文件路径，它位于 views/user/index.vue
// 确保这里的路径是正确的
import UserAdminFormPage from '@/views/UserAdmin/index.vue';
import UserAdminTable from '@/views/UserQuery/index.vue'; 


const userAdminRoute: RouteRecordRaw[] = [
    {
        path: '/user-admin', // 定义用户管理页面的父级路径
        name: 'UserAdmin', // 父级路由名称，通常与模块名一致
        // 如果用户管理模块需要一个通用的布局（例如包含侧边栏或顶部导航），
        // 则在这里引入你的布局组件。
        // 如果没有特定布局，也可以直接指向一个空组件或第一个子组件。
        component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
        meta: {
            locale: 'menu.userAdmin', // 侧边栏菜单的国际化 key (对应 src/locale 目录下的文件)
            requiresAuth: true, // 是否需要登录权限
            icon: 'icon-user', // 侧边栏菜单图标，这里用了一个示例图标 (Arco Design 的用户图标)
            order: 4, // 在侧边栏菜单中的排序，请根据你的需求调整 (数字越小越靠前)
            roles: ['admin'], // 可选：指定哪些角色可以访问，请根据你的权限设计调整
        },
        children: [
            {
                path: 'create', // 子路径，完整路径会是 /user-admin/create
                name: 'UserAdminCreate', // 创建用户表单页面的路由名称
                component: UserAdminFormPage, // 指向你之前编写的用户创建表单组件
                meta: {
                    locale: 'menu.userAdmin.create', // 页面在侧边栏或面包屑中的国际化 key
                    requiresAuth: true,
                    roles: ['admin'], // 示例：通常只有管理员角色可以创建用户，请根据你的权限设计调整
                },
            },
            //   如果你未来还有用户列表页、用户详情页、用户编辑页等，可以在这里继续添加子路由
                        {
                path: 'list', // 新增的子路径，完整路径会是 /user-admin/list
                name: 'UserAdminList', // 用户列表页面的路由名称
                component: UserAdminTable, // 指向你提供的用户列表组件
                meta: {
                    locale: 'menu.userAdmin.list', // 页面在侧边栏或面包屑中的国际化 key
                    requiresAuth: true,
                    roles: ['admin', 'user'], // 示例：管理员和普通用户可以查看用户列表
                },
            },
            
            // {
            //    path: 'edit/:id', // 动态路由参数，例如 /user-admin/edit/123
            //    name: 'UserAdminEdit',
            //    component: () => import('@/views/user/edit/index.vue'), // 假设用户编辑页面路径
            //    meta: {
            //      locale: 'menu.userAdmin.edit',
            //      requiresAuth: true,
            //      roles: ['admin'],
            //      hideInMenu: true, // 通常编辑页不在菜单中显示
            //    },
            // },
            // {
            //    path: ':id', // 动态路由参数，例如 /user-admin/123 (查看用户详情)
            //    name: 'UserAdminDetail',
            //    component: () => import('@/views/user/detail/index.vue'), // 假设用户详情页面路径
            //    meta: {
            //      locale: 'menu.userAdmin.detail',
            //      requiresAuth: true,
            //      roles: ['admin', 'user'],
            //      hideInMenu: true,
            //    },
            // },
        ],
    },
];

export default userAdminRoute;