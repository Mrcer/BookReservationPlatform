/*
    因为现在接口还不稳定，暂时假设接口返回数据格式如下，后面接口稳定后再修改
*/

import { getMockBookData } from '../types/book'
import { type BookData, type SearchQuery } from '@/types'

export const search = (query: SearchQuery): Promise<BookData[]> => {
  let books = getMockBookData()
  let result = books.filter((book) => book.title.includes(query.keyword))
  return Promise.resolve(result)
}
