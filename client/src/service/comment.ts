import service from './base'
import { commentUrl } from './api'
import type { CommentData } from '@/types'

export const sendComment = async (data: any) => {
  console.log(data)
  let req = service.post('/api/reviews', data)
  let serverData = (await req).data
  return serverData
}

interface dbCommentData {
  reviewId: number
  userId: number
  bookId: number
  content: string
  rating: number
  review_date: string
}

export const getComments = async (bookId: number) => {
  let req = service.get<dbCommentData[]>(commentUrl['get'](bookId))
  let serverData = (await req).data
  let result: CommentData[] = []
  for (let i = 0; i < serverData.length; i++) {
    result.push({
      comment_id: serverData[i].reviewId,
      user_id: serverData[i].userId,
      book_id: serverData[i].bookId,
      content: serverData[i].content,
      rating: serverData[i].rating,
      date: serverData[i].review_date,
    })
  }
  return result
}
