// frontend/src/api/device.ts <-- 文件名从 devices.ts 改为 device.ts
import axios from 'axios';
import qs from 'query-string';

export interface DeviceRecord {
    DeviceNo: string;
    DeviceName: string;
    DeviceUsage?: string;
    DStartTime?: string;
    DMT?: string;
    DStopTime?: string;
    // Operator?: string;
}

export interface DeviceParams extends Partial<DeviceRecord> {
    current: number;
    pageSize: number;
}

export interface DeviceListRes {
    list: DeviceRecord[];
    total: number;
}

/**
 * @description 获取设备列表
 * @param params 查询参数 (页码、每页大小、筛选条件)
 */
export function queryDeviceList(params: DeviceParams): Promise<DeviceListRes> {
    return axios.get('/api/device', { // <-- 路径改为 /api/device
        params,
        paramsSerializer: (obj) => {
            return qs.stringify(obj);
        },
    });
}

/**
 * @description 获取单个设备详情
 * @param deviceNo 设备编号
 */
export function queryDeviceDetail(deviceNo: string): Promise<DeviceRecord> {
    return axios.get(`/api/device/${deviceNo}`); // <-- 路径改为 /api/device/{id}
}

/**
 * @description 创建新设备
 * @param data 包含新设备信息的对象
 */
export function createDevice(data: DeviceRecord): Promise<any> {
    return axios.post('/api/device', data); // <-- 路径保持 /api/device (POST)
}

/**
 * @description 更新设备信息
 * @param deviceNo 设备编号
 * @param data 包含要更新字段的对象
 */
export function updateDeviceInfo(deviceNo: string, data: Partial<DeviceRecord>): Promise<any> {
    return axios.put(`/api/device/${deviceNo}`, data); // <-- 路径改为 /api/device/{id}
}

/**
 * @description 删除设备
 * @param deviceNo 设备编号
 */
export function deleteDevice(deviceNo: string): Promise<any> {
    return axios.delete(`/api/device/${deviceNo}`); // <-- 路径改为 /api/device/{id}
}