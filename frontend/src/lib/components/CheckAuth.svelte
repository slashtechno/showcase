import { onMount, onDestroy } from "svelte";
import { api } from "$lib/api/client";
import { user, signOut } from "$lib/user.svelte";
import type { Unsubscriber } from "svelte/store";

let unsubscribe: Unsubscriber;
let tokenVerified = false;

export function initializeAuth() {
    onMount(() => {
        if (user.isAuthenticated) {
            console.debug('User is already authenticated');
            return;
        }

        const token = localStorage.getItem('token');
        if (token) {
            console.debug('Token found in localStorage', token);
            
        } else {
            console.debug('No token found in localStorage');
        }

    //     unsubscribe = user.subscribe((value) => {
    //         const token = value.token;
    //         if (api.tokenSet && !tokenVerified) {
    //             api.verifyAuth().then((response) => {
    //                 localStorage.setItem('token', token);
    //                 user.set({ email: response.email, token: token, isAuthenticated: true });
    //                 console.debug('Token verified, setting user in store', token);
    //                 tokenVerified = true;
    //             }).catch((err) => {
    //                 console.log('Token is invalid', err);
    //                 signOut();
    //             });
    //         } else if (!token) {
    //             console.log('No token found');
    //         }
    //     });
    // });

    // onDestroy(() => {
    //     if (unsubscribe) {
    //         console.debug('Unsubscribing from user store');
    //         unsubscribe();
    //     }
    // });
}
