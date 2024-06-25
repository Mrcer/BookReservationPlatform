import type { ReservationData } from '@/types'
import { reservationUrl } from './api'
import service from './base'

// 提交预约，需要登录
export const submitReservation = async (
  uid: number,
  bookId: number,
  reservationLocation: string
) => {
  let req = await service.post<{
    message: string
    reservationId: number
  }>(reservationUrl['submit'], {
    userId: uid,
    bookId,
    reservation_location: reservationLocation,
  })
  return req.data
}

// 获取预约详情，需要登录
export const getReservation = async (reservationId: number) => {
  let req = await service.get<ReservationData>(reservationUrl['get'](reservationId))
  return req.data
}

// 获取所有已确认的预约，需要登录
export const getAllConfirmedReservations = async (uid: number) => {
  let req = await service.get<ReservationData[]>(reservationUrl['getAllComfirmed'])
  return req.data
}

// 获取用户的所有预约，需要登录
export const getUserReservations = async (uid: number) => {
  let req = await service.get<ReservationData[]>(reservationUrl['getUserReservations'](uid))
  return req.data
}

// 取消预约，需要登录
export const cancelReservation = async (reservationId: number) => {
  let req = await service.put(reservationUrl['cancel'](reservationId))
  return req.data
}

// 更新预约，需要管理员权限
export const updateReservation = async (data: ReservationData) => {
  let req = await service.put(reservationUrl['update'](data.reservationId), data)
  return req.data
}

// 删除预约，需要管理员权限
export const deleteReservation = async (reservationId: number) => {
  let req = await service.delete(reservationUrl['delete'](reservationId))
  return req.data
}

// 完成预约，需要管理员权限
export const completeReservation = async (reservationId: number) => {
  let req = await service.put(reservationUrl['complete'](reservationId))
  return req.data
}
