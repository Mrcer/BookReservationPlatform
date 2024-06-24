import Mock from "mockjs";
import { commentUrl } from '@/service/api'
 
export const sendSuccessfully = Mock.mock(import.meta.env.VITE_API_URL+commentUrl.sendComment, "post", {
    message: "Review added successfully", 
    reviewId: 1
});

export const fetchComments = Mock.mock(import.meta.env.VITE_API_URL + commentUrl['get'](1), "get", 
    [ {reviewId:1, userId:1, bookId:1, content:"This is a good book", rating:5, review_date:"2022-01-01T00:00:00.000Z"},
    {reviewId:2, userId:2, bookId:1, content:"This is a bad book", rating:1, review_date:"2022-01-02T00:00:00.000Z"},
    {reviewId:3, userId:3, bookId:1, content:"This is a great book", rating:4, review_date:"2022-01-03T00:00:00.000Z"}
    ]  
);