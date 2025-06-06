import { RouteRecordRaw } from 'vue-router';

// 导入你的设备表单组件
// 确保路径正确，@ 通常指向 src 目录
import DeviceForm from '@/views/Device/index.vue'; // 这是我们之前编写的设备表单组件

const deviceRoutes: RouteRecordRaw[] = [
    {
        path: '/device', // 设备管理页面的父级路径
        name: 'deviceParent', // 父级路由名称
        component: () => import('@/layout/default-layout.vue'), // 引用布局组件
        meta: {
            locale: 'menu.device', // 侧边栏菜单的国际化 key
            requiresAuth: true, // 需要登录权限
            icon: 'icon-desktop', // 设备管理图标，您可以根据 Arco Design 图标库选择合适的图标
            order: 3, // 在侧边栏菜单中的排序 (数字越小越靠前)
        },
        children: [
            {
                path: 'add', // 子路径，完整路径会是 /device/add
                name: 'deviceAdd', // 页面路由名称
                component: DeviceForm, // 设备表单组件
                meta: {
                    locale: 'menu.device.form', // 页面在侧边栏或面包屑中的国际化 key
                    requiresAuth: true,
                    roles: ['admin', 'user'], // 可选：指定哪些角色可以访问
                },
            },
            // 如果您有设备列表、设备详情等其他与设备相关的页面，
            // 可以在这里作为 '/device' 的子路由继续添加。
            // 例如：
            // {
            //   path: 'list',
            //   name: 'deviceList',
            //   component: () => import('@/views/DeviceList.vue'),
            //   meta: {
            //     locale: 'menu.device.list',
            //     requiresAuth: true,
            //     roles: ['admin', 'user'],
            //   },
            // },
        ],
    },
];

export default deviceRoutes;