import service from './base'
import {commentUrl} from './api'
import type {CommentData} from '@/types'

export const sendComment = async (data: any) => {
    console.log(data)
    let req = service.post("/api/reviews", data)
    let serverData = (await req).data
    return serverData    
}

export const getComments = async (bookId: number) => {
    let req = service.get<CommentData[]>(commentUrl['get'](bookId))
    let serverData = (await req).data
    return serverData
}