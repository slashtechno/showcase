import { writable } from "svelte/store";

type User = {
    email: string;
    token: string;
};

export const user = writable<User>({
    email: "",
    token: ""
});