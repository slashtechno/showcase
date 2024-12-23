<svelte:options runes />

<script lang="ts">
import { onMount, onDestroy } from "svelte";
import { api } from "$lib/api/client.svelte";
import { user, signOut } from "$lib/user.svelte";
import type { Unsubscriber } from "svelte/store";

let unsubscribe: Unsubscriber;

    onMount(() => {
        if (user.isAuthenticated) {
            console.debug('User is already authenticated, checking token');
            validateToken(user.token);
            return;
        }

        const token = localStorage.getItem('token');
        if (token) {
            console.debug('Token found in localStorage', token);
            validateToken(token);
        } else {
            console.debug('No token found in localStorage');
        }
    });

    onDestroy(() => {
        if (unsubscribe) {
            console.debug('Unsubscribing from user store');
            unsubscribe();
        }
    });

    function validateToken(token: string) {
        api.verifyAuth(token).then((response) => {
            // Since it's $state we can do this. Assigning to user directly will not work as it's an import
            user.email = response.email;
            user.token = token;
            user.isAuthenticated = true;
            console.debug('Token verified, setting user in store', token);
        }).catch((err) => {
            console.log('Token is invalid', err);
            signOut();
        });
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
</script>