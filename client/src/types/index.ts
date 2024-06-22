import type { Failed } from '@element-plus/icons-vue'

export interface BookData {
  id: number
  title: string
  author: string
  publisher: string
  publishDate: string
  isbn: string
  location: string
  status: BookStatus
}

export enum BookStatus {
  Available = 'available',
  Reserved = 'reserved',
  Borrowed = 'borrowed',
  Damaged = 'damaged',
}

export interface AtivityData {
  id: number
  name: string
  description: string
}

export interface CommentData {
  comment_id: number
  user_id: number
  book_id: number
  content: string
  rating: number
  date: string
}

export interface ReservationData {
  reservation_id: number
  user_id: number
  book_id: number
  reserved_date: string
  status: ReservationStatus
}

export enum ReservationStatus {
  Comfirmed = 'confirmed',
  Cancelled = 'cancelled',
  Completed = 'completed',
  Failed = 'failed',
}

export interface SearchQuery {
  keyword: string
}