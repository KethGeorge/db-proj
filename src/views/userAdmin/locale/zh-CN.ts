// frontend/src/locale/zh-CN.ts
export default {
  // ... (其他现有模块的翻译) ...
  'User': '用户管理',
  'User.list': '用户列表',
  'menu.userAdmin': '用户管理',
  'menu.userAdmin.list': '用户列表',
  'menu.userAdmin.create': '新建用户',
  'menu.userAdmin.edit': '编辑用户',
  'menu.userAdmin.view': '用户详情',
  'userAdmin.list': '用户列表',

  // --- UserForm.vue 和 UserList.vue 的表单字段相关键 ---
  'userAdmin.form.label.UserNo': '账户编号',
  'userAdmin.form.placeholder.UserNo':
    '请输入账户编号（8字符以内，留空则后端生成）',
  'userAdmin.form.UserNo': '账户编号',
  'userAdmin.form.UserNo.placeholder':
    '请输入账户编号（8字符以内，留空则后端生成）',
  'userAdmin.form.label.UserName': '账户名',
  'userAdmin.form.placeholder.UserName': '请输入账户名（20字符以内）',
  'userAdmin.form.UserName': '账户名',
  'userAdmin.form.UserName.placeholder': '请输入账户名（20字符以内）',
  'userAdmin.form.label.UserPassword': '账户密码',
  'userAdmin.form.placeholder.UserPassword': '请输入账户密码',
  'userAdmin.form.label.NewUserPassword': '新密码',
  'userAdmin.form.placeholder.NewUserPassword': '请输入新密码（留空则不修改）',
  'userAdmin.form.label.UserPermissions': '账户权限',
  'userAdmin.form.UserPermissions': '账户权限',
  'userAdmin.form.UserPermissions.placeholder':
    '请选择账户权限（留空则不修改）',
  'userAdmin.form.placeholder.UserPermissions': '请选择账户权限',
  'userAdmin.form.Email': '用户邮箱',
  'userAdmin.form.placeholder.Email': '请输入用户邮箱（20字符以内）',
  'userAdmin.form.label.Email': '用户邮箱',
  'userAdmin.form.Email.placeholder': '请输入用户邮箱（20字符以内）',
  'userAdmin.form.Telephone': '用户电话',
  'userAdmin.form.placeholder.Telephone': '请输入用户电话（13字符以内）',
  'userAdmin.form.Telephone.placeholder': '请输入用户电话（13字符以内）',
  'userAdmin.form.label.Telephone': '用户电话',
  'userAdmin.form.UserNo.placeholder.notCreate': '请输入用户编号（8字符以内）',
  // --- UserList.vue 的搜索和操作按钮键 ---
  'userAdmin.form.search': '查询',
  'userAdmin.form.reset': '重置',
  'userAdmin.operation.create': '新建用户',
  'userAdmin.actions.refresh': '刷新',
  'userAdmin.actions.density': '密度',
  'userAdmin.actions.columnSetting': '列设置',
  'userAdmin.columns.operations.viewLogs': '修改记录', // 按钮文本
  'userAdmin.logViewer.title': '用户 [{name}] 的修改记录', // 弹窗标题
  // --- UserList.vue 的表格列头键 ---
  'userAdmin.columns.index': '#',
  'userAdmin.columns.UserNo': '账户编号',
  'userAdmin.columns.UserName': '账户名',
  'userAdmin.columns.UserPermissions': '账户权限',
  'userAdmin.columns.Email': '用户邮箱',
  'userAdmin.columns.Telephone': '用户电话',
  'userAdmin.columns.operations': '操作',
  'userAdmin.columns.operations.view': '查看',
  'userAdmin.columns.operations.edit': '编辑',
  'userAdmin.columns.operations.delete': '删除',

  // --- UserForm.vue 和 UserList.vue 的用户权限选项键 ---
  'userAdmin.form.UserPermissions.admin': '管理员',
  'userAdmin.form.UserPermissions.user': '普通用户',
  'userAdmin.form.UserPermissions.guest': '访客',
  'userAdmin.form.UserPermissions.undefined': '未定义',
  'userAdmin.form.selectDefault': '请选择',

  // --- UserList.vue 的表格密度选项键 ---
  'userAdmin.size.mini': '迷你',
  'userAdmin.size.small': '偏小',
  'userAdmin.size.medium': '中等',
  'userAdmin.size.large': '偏大',

  // --- UserForm.vue 的页面标题键 ---
  'userAdmin.form.title.create': '新建用户',
  'userAdmin.form.title.edit': '编辑用户',
  'userAdmin.form.title.view': '查看用户',
  'userAdmin.form.title.default': '用户信息',

  // --- UserForm.vue 的表单校验消息键 (根据字段长度和要求重新确认) ---
  'userAdmin.form.validation.UserNoRequired': '账户编号不能为空',
  'userAdmin.form.validation.UserNoLength': '账户编号长度为8个字符', // 明确指出是8个字符
  'userAdmin.form.validation.UserNameRequired': '账户名不能为空',
  'userAdmin.form.validation.UserNameLength': '账户名长度不能超过20个字符',
  'userAdmin.form.validation.UserPasswordRequired': '账户密码不能为空',
  'userAdmin.form.validation.UserPasswordLength': '密码不能少于6位',
  'userAdmin.form.validation.UserPasswordMaxLength': '密码长度不能超过20个字符',
  'userAdmin.form.validation.EmailInvalid': '请输入有效的邮箱地址',
  'userAdmin.form.validation.EmailLength': '邮箱长度不能超过20个字符',
  'userAdmin.form.validation.UserPermissionsLength': '权限长度不能超过5个字符',
  'userAdmin.form.validation.TelephoneLength': '电话长度不能超过13个字符',
  'userAdmin.form.validation.UserNoExists': '账户编号已存在，请使用其他编号',
  'userAdmin.form.validation.UserNameExists': '账户名已存在，请使用其他账户名',
  'userAdmin.form.validation.EmailExists': '邮箱已存在，请使用其他邮箱',

  // --- UserList.vue 和 UserForm.vue 的通用消息键 ---
  'userAdmin.message.idMissingForView': '缺少用户编号，无法查看。',
  'userAdmin.message.idMissingForEdit': '缺少用户编号，无法编辑。',
  'userAdmin.message.idMissingForDelete': '缺少用户编号，无法删除。',
  'userAdmin.message.idMissingForUpdate': '缺少用户编号，无法更新。',
  'userAdmin.message.createSuccess': '用户创建成功！',
  'userAdmin.message.updateSuccess': '用户信息更新成功！',
  'userAdmin.message.deleteSuccess': '用户删除成功！',
  'userAdmin.message.deleteFail': '用户删除失败',
  'userAdmin.message.confirmDelete': '确定要删除此用户吗？',
  'userAdmin.message.fetchFail': '获取用户信息失败',

  // --- 通用表单操作键 (groupForm 通常是独立于模块的) ---
  'groupForm.reset': '重置',
  'groupForm.submit': '提交',
  'groupForm.save': '保存',
  'groupForm.back': '返回',
  'groupForm.validationWarning': '请检查并填写所有必填项！',
  'groupForm.operationFail': '操作失败',
  'groupForm.noDescription': '无描述',
};
