import type { Failed } from '@element-plus/icons-vue'

export interface BookData {
  id: number
  cover: string
  title: string
  author: string
  publisher: string
  publishDate: string
  isbn: string
  location: string
  status: BookStatus
  rating: number
}

export enum BookStatus {
  Available = 'available',
  Reserved = 'reserved',
  Borrowed = 'borrowed',
  Damaged = 'damaged',
}

export interface ActivityData {
  activityId: number
  name: string
  description: string
  start_time: string
  end_time: string
  location: string
  link: string
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
  reservationId: number
  userId: number
  bookId: number
  reserved_date: string
  status: ReservationStatus
  book_location: string
  reservation_location: string
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

export enum UserRole {
  Student = 'student',
  Teacher = 'teacher',
  Admin = 'admin',
}

export interface RegisterForm {
  username: string
  email: string
  password: string
  role: UserRole
}

export interface UserInfo {
  id: number
  username: string
  email: string
  credit: number
  registration_date: string
  role: UserRole
}
