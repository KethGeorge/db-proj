export type RoleType = '' | '*' | 'admin' | 'user';
export interface UserState {
  name?: string;
  accountId?: string;
  certification?: number;
  role: RoleType;
}
