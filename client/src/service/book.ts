import { BookStatus, type BookData } from '@/types'
import service from './base'
import { bookUrl } from './api'

interface InfoResponse {
  bookId: number
  title: string
  author: string
  publisher: string
  publish_date: string
  isbn: string
  location: string
  status: BookStatus
  reservation_count: number
  borrower_id: number
  book_image: string
  average_rating: number
}

const serverInfo2BookData = (serverData: InfoResponse): BookData => {
  return {
    id: serverData.bookId,
    cover: serverData.book_image,
    title: serverData.title,
    author: serverData.author,
    publisher: serverData.publisher,
    publishDate: serverData.publish_date,
    isbn: serverData.isbn,
    location: serverData.location,
    status: serverData.status,
    rating: serverData.average_rating,
  }
}

// 查看图书详情
export const getInfo = async (id: number): Promise<BookData> => {
  let req = service.get<InfoResponse>(bookUrl['getInfo'](id))
  let serverData = (await req).data
  return serverInfo2BookData(serverData)
}

// 搜索图书
export const search = async (query: string): Promise<BookData[]> => {
  let req = service.get<InfoResponse[]>(bookUrl['search'], { params: { query } })
  let serverData = (await req).data
  return serverData.map(serverInfo2BookData)
}

// 获取图书状态
export const getStatus = async (id: number) => {
  let req = await service.get<{status: BookStatus}>(bookUrl['getStatus'](id))
  return req.data.status
}

// 获取借阅图书
export const getBorrowed = async (uid: number) => {
  let req = await service.get<InfoResponse[]>(bookUrl['getBorrowed'](uid))
  return req.data.map(serverInfo2BookData)
}

export interface AddParams {
  title: string
  author: string
  publisher: string
  publish_date: string
  isbn: string
  location: string
  book_image: string // base64 encoded image
}

// 添加图书，需要管理员权限
export const add = async (params: AddParams) => {
  let req = await service.post(bookUrl['add'], params)
  return req.data
}

// 更新图书信息，需要管理员权限
export const updateInfo = async (id: number, params: AddParams) => {
  let req = await service.put(bookUrl['updateInfo'](id), params)
  return req.data
}

// 更新图书状态，需要管理员权限
export const updateStatus = async (id: number, status: BookStatus) => {
  let req = await service.put(bookUrl['updateStatus'](id), { status })
  return req.data
}

// 删除图书，需要管理员权限
export const deleteBook = async (id: number) => {
  let req = await service.delete(bookUrl['delete'](id))
  return req.data
}

// 借阅图书，需要登录
export const borrowBook = async (id: number, uid: number) => {
  let req = await service.post(bookUrl['borrow'](id), { userId: uid })
  return req.data
}