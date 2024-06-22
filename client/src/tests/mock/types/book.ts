import { type BookData, BookStatus } from '@/types'
import { imagePlaceholder } from '.'

export const getMockBookData = () => {
  let result: BookData[] = []
  let mockCover = 'data:image/png;base64,' + imagePlaceholder
  result.push({
    id: 1,
    title: 'The Great Gatsby',
    author: 'F. Scott Fitzgerald',
    publisher: "Charles Scribner's Sons",
    publishDate: '1925-04-01',
    rating: 4.5,
    isbn: '9780743273565',
    location: 'New York',
    cover: mockCover,
    status: BookStatus.Available,
  })
  result.push({
    id: 2,
    title: 'To Kill a Mockingbird',
    author: 'Harper Lee',
    publisher: 'J. B. Lippincott & Co.',
    publishDate: '1960-07-01',
    rating: 4.2,
    isbn: '9780446310789',
    location: 'New York',
    cover: mockCover,
    status: BookStatus.Reserved,
  })
  result.push({
    id: 3,
    title: '1984',
    author: 'George Orwell',
    publisher: 'Secker & Warburg',
    publishDate: '1949-06-01',
    rating: 4.1,
    isbn: '9780451524935',
    location: 'New York',
    cover: mockCover,
    status: BookStatus.Borrowed,
  })
  result.push({
    id: 4,
    title: 'Pride and Prejudice',
    author: 'Jane Austen',
    publisher: 'Little, Brown and Company',
    publishDate: '1813-07-01',
    rating: 4.3,
    isbn: '9780316769484',
    location: 'New York',
    cover: mockCover,
    status: BookStatus.Damaged,
  })
  return result
}
