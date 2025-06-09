// src/locale/zh-CN.ts
export default {
  // ... (所有现有翻译) ...
  'menu.report': '实验报告',
  'menu.report.list': '报告列表',
  'menu.report.view': '报告详情',
  'menu.experimentAdmin.conduct': '执行实验',
  'menu.experimentAdmin.report': '实验报告详情', // 新增菜单/面包屑标题

  // ...
  'experiment.columns.operations.delete': '删除',
  'experiment.columns.operations.report': '查看报告', // 新增按钮文本

  // ...
  'experiment.message.fetchFail': '获取实验记录信息失败',

  'report.list.search': '查询',
  'report.list.reset': '重置',
  'report.list.label.ExperimentCode': '报告编码',
  'report.list.placeholder.ExperimentCode': '请输入报告编码',
  'report.list.label.ExperimentNo': '实验编号',
  'report.list.placeholder.ExperimentNo': '请输入实验编号',
  'report.list.label.ExperimentName': '实验名称',
  'report.list.placeholder.ExperimentName': '请输入实验名称',

  'report.list.columns.ExperimentCode': '报告编码',
  'report.list.columns.ExperimentNo': '实验编号',
  'report.list.columns.ExperimentName': '实验名称',
  'report.list.columns.ExperimentalStatus': '实验状态',
  'report.list.columns.operations': '操作',
  'report.list.operations.view': '查看详情',

  // --- 新增实验报告相关翻译 ---
  'experiment.report.title': '实验报告详情',
  'experiment.report.hecTitle': '加热实验数据',
  'experiment.report.mecTitle': '搅拌实验数据',
  'experiment.report.mtecTitle': '测定实验数据',
  'experiment.report.noHecData': '暂无加热实验数据',
  'experiment.report.noMecData': '暂无搅拌实验数据',
  'experiment.report.noMtecData': '暂无测定实验数据',
  'experiment.report.fetchFail': '获取实验报告失败，请稍后重试。',
  'experiment.report.yes': '是',
  'experiment.report.no': '否',

  // 报告主表单字段
  'experiment.report.label.ExperimentCode': '报告编码',
  'experiment.report.label.ExperimentNo': '关联实验编号',
  'experiment.report.label.ExperimentName': '实验名称',
  'experiment.report.label.ExperimentalStatus': '实验状态',

  // HEC 字段
  'experiment.report.label.HEC': '加热实验序号',
  'experiment.report.label.Temperature': '温度',
  'experiment.report.label.Time1': '时间',
  'experiment.report.label.SafeArea': '安全温度阈值',

  // MEC 字段
  'experiment.report.label.MEC': '搅拌实验序号',
  'experiment.report.label.HeightError': '高度误差',
  'experiment.report.label.PlainError': '水平误差',
  'experiment.report.label.ErrorArea': '误差阈值',
  'experiment.report.label.SpeedError': '速度误差',
  'experiment.report.label.Time2': '时间',

  // MTEC 字段
  'experiment.report.label.MTEC': '测定实验序号',
  'experiment.report.label.PhotoPath': '照片路径',
  'experiment.report.label.IsGel': '是否凝固',
  'experiment.report.label.Time3': '时间',

  // ... (文件剩余部分) ...
};
