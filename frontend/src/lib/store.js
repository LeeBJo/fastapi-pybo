import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {               // 지속성 스토어 : 웨브라우져 새로고침 후에도 store값 유지
    const storedValueStr = localStorage.getItem(key)
    const store = writable(storedValueStr != null ? JSON.parse(storedValueStr) : initValue)
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val))
    })
    return store
}
//유저리스트 페이지 변수 추가
export const page = persist_storage("page", 0)  
export const keyword = persist_storage("keyword", 0)
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const id = persist_storage("id", 0)
export const is_login = persist_storage("is_login", false)
export const is_admin = persist_storage("is_admin", false)
//export const userpage = persist_storage("userpage", 0)