import Mock from "mockjs";
import { bookUrl } from '@/service/api'
import { imagePlaceholder } from './types/index'
import { type BookData, BookStatus } from '@/types'

export const getBookInfo1 = Mock.mock(import.meta.env.VITE_API_URL+bookUrl.getInfo(1), "get", {
    bookId: 1,
    title: 'The Great Gatsby',
    author: 'F. Scott Fitzgerald',
    publisher: "Charles Scribner's Sons",
    publish_date: '1925-04-01',
    average_rating: 4.5,
    isbn: '9780743273565',
    location: 'New York',
    book_image: 'data:image/png;base64,' + imagePlaceholder,
    status: BookStatus.Available,
});