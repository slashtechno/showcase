import { writable } from "svelte/store";

interface User {
    email: string;
    token: string;
}

export const user = writable<User | null>({
    email: "",
    token: ""
});
