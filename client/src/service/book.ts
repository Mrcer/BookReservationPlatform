import type { BookData, BookStatus } from "@/types"
import service from "./base"
import { bookUrl } from "./api"

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

const getInfo = async (id: number): Promise<BookData> => {
    let req = service.get<InfoResponse>(bookUrl["getInfo"](id))
    let serverData = (await req).data
    let bookData: BookData = {
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
    return bookData
}

export { getInfo }