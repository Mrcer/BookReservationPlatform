import type {ActivityData} from '@/types'
import service from "./base"
import { activityUrl } from './api'

// 查看活动
const getActivityList = async () => {
    let req = await service.get<ActivityData>(activityUrl['getAll'])
    return req.data
}

// 查看活动详情
const getDetail = async (id: number) => {
    let req = await service.get<ActivityData>(activityUrl['getDetail'](id))
    return req.data
}

// 添加活动，需要管理员权限
const add = async (data: ActivityData) => {
    let req = await service.post<ActivityData>(activityUrl['add'], data)
    return req.data
}

// 更新活动，需要管理员权限
const update = async (id: number, data: ActivityData) => {
    let req = await service.put<ActivityData>(activityUrl['update'](id), data)
    return req.data
}

// 删除活动，需要管理员权限
const remove = async (id: number) => {
    let req = await service.delete(activityUrl['delete'](id))
    return req.data
}

export { getActivityList, getDetail, add, update, remove }