import { RouteRecordRaw } from 'vue-router';

// 导入你的 ExperimentStart 组件
// 确保路径正确，@ 通常指向 src 目录
import ExperimentStart from '@/views/ExperimentView.vue';

const experimentRoute: RouteRecordRaw[] = [
  {
    path: '/experiment', // 可以定义一个父级路径，或者直接用你的页面路径
    name: 'experiment', // 父级路由名称 (可选)
    component: () => import('@/layout/default-layout.vue'), // 如果有布局组件，通常在这里引入
    meta: {
      locale: 'menu.experiment', // 侧边栏菜单的国际化 key (对应 src/locale 目录下的文件)
      requiresAuth: true, // 是否需要登录权限
      icon: 'icon-bulb', // 侧边栏菜单图标 (对应 Arco Design 图标库)
      order: 3, // 在侧边栏菜单中的排序 (数字越小越靠前)
    },
    children: [
      {
        path: 'start', // 子路径，完整路径会是 /experiment/start
        name: 'experimentStart', // 页面路由名称
        component: ExperimentStart, // 页面组件
        meta: {
          locale: 'menu.experiment.start', // 页面在侧边栏或面包屑中的国际化 key
          requiresAuth: true,
          roles: ['admin', 'user'], // 可选：指定哪些角色可以访问
        },
      },
    ],
  },
];

export default experimentRoute;
