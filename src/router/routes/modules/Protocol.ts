import { RouteRecordRaw } from 'vue-router';

// 导入你的 Protocol 表单组件
// 根据你之前提供的文件路径，假设它位于 views/protocol/index.vue
// 确保这里的路径是正确的
import ProtocolFormPage from '@/views/Protocol/index.vue';

const protocolRoute: RouteRecordRaw[] = [
  {
    path: '/protocol', // 定义 Protocol 页面的父级路径
    name: 'Protocol', // 父级路由名称，通常与模块名一致
    // 如果 Protocol 模块需要一个通用的布局，例如包含侧边栏或顶部导航，
    // 则在这里引入你的布局组件。
    // 如果没有特定布局，也可以直接指向一个空组件或第一个子组件。
    component: () => import('@/layout/default-layout.vue'), // 假设你有一个默认布局组件
    meta: {
      locale: 'menu.protocol', // 侧边栏菜单的国际化 key (对应 src/locale 目录下的文件)
      requiresAuth: true, // 是否需要登录权限
      icon: 'icon-settings', // 侧边栏菜单图标，这里用了一个示例图标，请根据 Arco Design 图标库选择
      order: 5, // 在侧边栏菜单中的排序，请根据你的需求调整 (数字越小越靠前)
    },
    children: [
      {
        path: 'create', // 子路径，完整路径会是 /protocol/create
        name: 'ProtocolCreate', // 表单页面的路由名称
        component: ProtocolFormPage, // 指向你之前编写的 Protocol 表单组件
        meta: {
          locale: 'menu.protocol.create', // 页面在侧边栏或面包屑中的国际化 key
          requiresAuth: true,
          roles: ['admin', 'user'], // 可选：指定哪些角色可以访问，请根据你的权限设计调整
        },
      },
      // 如果你未来还有 Protocol 的列表页、详情页等，可以在这里继续添加子路由
      // {
      //   path: 'list',
      //   name: 'ProtocolList',
      //   component: () => import('@/views/protocol/list/index.vue'),
      //   meta: {
      //     locale: 'menu.protocol.list',
      //     requiresAuth: true,
      //     roles: ['admin', 'user'],
      //   },
      // },
      // {
      //   path: ':id', // 动态路由参数，例如 /protocol/123
      //   name: 'ProtocolDetail',
      //   component: () => import('@/views/protocol/detail/index.vue'),
      //   meta: {
      //     locale: 'menu.protocol.detail',
      //     requiresAuth: true,
      //     hideInMenu: true, // 通常详情页不在菜单中显示
      //   },
      // },
    ],
  },
];

export default protocolRoute;