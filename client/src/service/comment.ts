import service from './base'
import {commentUrl} from './api'

export const sendComment = async (data: any) => {
    console.log(data)
    let req = service.post("/api/reviews", data)
    let serverData = (await req).data
    return serverData    
}