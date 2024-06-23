import Mock from "mockjs";
import { commentUrl } from '@/service/api'
 
export const sendSuccessfully = Mock.mock(import.meta.env.VITE_API_URL+commentUrl.sendComment, "post", {
    message: "Review added successfully", 
    reviewId: 1
});