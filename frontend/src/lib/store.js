import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {               // 지속성 스토어 : 웨브라우져 새로고침 후에도 store값 유지
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}

export const page = persist_storage("page", 0)  
export const keyword = persist_storage("keyword", 0)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)