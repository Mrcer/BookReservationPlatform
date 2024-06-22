import Book from '@/components/Home/Book.vue'
import { getMockBookData } from '@/tests/mock/types/book'
import { describe, test, expect, beforeAll } from 'vitest'
import { mount } from '@vue/test-utils'

const mockData = getMockBookData()

describe('Book.vue', () => {
  test('挂载', () => {
    const wrapper = mount(Book, {
      props: {
        book: mockData[0],
      },
    })
    expect(wrapper.exists()).toBe(true)
  }),
    test('图书信息', () => {
      const wrapper = mount(Book, {
        props: {
          book: mockData[0],
        },
      })
      expect(wrapper.get('[data-test="author"]').text()).toBe('作者：' + mockData[0].author)
      expect(wrapper.get('[data-test="title-link"]').text()).toBe(mockData[0].title)
      expect(wrapper.get('[data-test="publisher"]').text()).toBe('出版社：' + mockData[0].publisher)
      expect(wrapper.get('[data-test="publishDate"]').text()).toBe(
        '出版日期：' + mockData[0].publishDate
      )
    }),
    test('点击图书链接', () => {
      // TODO: 需要使用 mock-router 进行测试
      // ref: https://test-utils.vuejs.org/guide/advanced/vue-router.html
    }),
    test('预约图书事件', () => {
      const wrapper = mount(Book, {
        props: {
          book: mockData[0],
        },
      })
      let reserve_btn = wrapper.getComponent('[data-test="reserve-btn"]') as any
      reserve_btn.trigger('click')
      let reserve_event = wrapper.emitted('reserve') as any
      expect(reserve_event).toHaveLength(1)
      expect(reserve_event[0]).toEqual([mockData[0].id])
    }),
    test('按键样式', async () => {
      const wrapper = mount(Book, {
        props: {
          book: mockData[0],
        },
      })
      let reserve_btn = wrapper.getComponent('[data-test="reserve-btn"]') as any
      expect(reserve_btn.text()).toBe('预约')
      expect(reserve_btn.props().disabled).toBe(false)
      await wrapper.setProps({ book: mockData[1] })
      expect(reserve_btn.text()).toBe('预约')
      expect(reserve_btn.props().disabled).toBe(false)
      await wrapper.setProps({ book: mockData[2] })
      expect(reserve_btn.text()).toBe('已借出')
      expect(reserve_btn.props().disabled).toBe(true)
      await wrapper.setProps({ book: mockData[3] })
      expect(reserve_btn.text()).toBe('无法借阅')
      expect(reserve_btn.props().disabled).toBe(true)
    })
})
