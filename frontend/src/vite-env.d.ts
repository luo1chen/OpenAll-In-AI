/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}

// Element Plus 自动导入组件类型声明
declare module 'element-plus' {
  import { DefineComponent } from 'vue'
  export const ElButton: DefineComponent<any, any, any>
  export const ElInput: DefineComponent<any, any, any>
  export const ElSelect: DefineComponent<any, any, any>
  export const ElOption: DefineComponent<any, any, any>
  export const ElCard: DefineComponent<any, any, any>
  export const ElTabs: DefineComponent<any, any, any>
  export const ElTabPane: DefineComponent<any, any, any>
  export const ElUpload: DefineComponent<any, any, any>
  export const ElIcon: DefineComponent<any, any, any>
  export const ElMessage: any
  export const ElSlider: DefineComponent<any, any, any>
  export const ElForm: DefineComponent<any, any, any>
  export const ElFormItem: DefineComponent<any, any, any>
  export const ElPageHeader: DefineComponent<any, any, any>
  export const ElImage: DefineComponent<any, any, any>
  export const ElTag: DefineComponent<any, any, any>
  export const Plus: DefineComponent<any, any, any>
  export const Delete: DefineComponent<any, any, any>
  export const User: DefineComponent<any, any, any>
  export const Robot: DefineComponent<any, any, any>
  export const ChatDotRound: DefineComponent<any, any, any>
  export const Picture: DefineComponent<any, any, any>
}