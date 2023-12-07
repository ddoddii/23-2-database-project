import { writable } from 'svelte/store'

const persist_storage = (key, initValue) => {
    const storedValueStr = localStorage.getItem(key)

    let parsedValue;
    if (storedValueStr === null || storedValueStr === "undefined") {
        parsedValue = initValue;
    } else {
        try {
            parsedValue = JSON.parse(storedValueStr);
        } catch (e) {
            console.error("Error parsing JSON from localStorage:", e);
            parsedValue = initValue;
        }
    }

    const store = writable(parsedValue);
    store.subscribe((val) => {
        localStorage.setItem(key, JSON.stringify(val));
    });
    return store;

}



export const page = persist_storage("page", 0)
export const keyword = persist_storage("keyword", "")
export const access_token = persist_storage("access_token", "")
export const username = persist_storage("username", "")
export const is_login = persist_storage("is_login", false)

