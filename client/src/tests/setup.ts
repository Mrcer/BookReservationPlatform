import { config } from '@vue/test-utils'
import ElementPlus from 'element-plus'
import router from '@/router'
import 'element-plus/dist/index.css'

config.global.plugins.push(ElementPlus)
config.global.plugins.push(router)
