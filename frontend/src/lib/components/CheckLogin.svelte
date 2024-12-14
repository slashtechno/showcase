<!-- If the user is logged in, display a welcome message and a sign out button. Otherwise, display a button linking to the login page. -->
<!-- <svelte:options runes /> -->
<script lang="ts">
    // import { onDestroy, onMount } from "svelte";
    // import {api} from "$lib";
    import {user} from "$lib/stores";
    // import type { Unsubscriber } from "svelte/store";

    // let unsubscribe: Unsubscriber;
    // let tokenVerified = false;

    function signOut() {
        console.log('Signing out');
        // Clear auth state
        user.set({ email: '', token: '' });
        // Remove token from localStorage
        localStorage.removeItem('token');
    }

    
    // onMount(() => {
    //     if (localStorage.getItem('token')) {
    //         // If token is present in localStorage, set it in the store
    //         user.set({ email: "",token: localStorage.getItem('token')! });
    //     }
    //     // Subscribe to user store
    //     unsubscribe = user.subscribe((value) => {
    //         const token = value.token; 
    //         if (token && !tokenVerified) {
    //             // Check if the token is present in the store and verify it if it hasn't already
    //             // Check if token is valid
    //             api.verifyAuth(token).then((response) => {
    //                 console.log('Token is valid');
    //                 localStorage.setItem('token', token);
    //                 user.set({email: response.email, token: token});
    //                 tokenVerified = true;
    //             }).catch((err) => {
    //                 console.log('Token is invalid', err);
    //                 signOut();
    //             });
    //         } else if (!token) {
    //             // If the token is not present in the store or localStorage, log that
    //             console.log('No token found');
    //         }
    //     });
    // });

    // onDestroy(() => {
    //     // Unsubscribe from user store if it exists
    //     // For some reason this seems to sometimes get called before onMount
    //     if (unsubscribe) {
    //         console.debug('Unsubscribing from user store');
    //         unsubscribe();
    //     }
    // });
</script>

{#if $user.token}
    <div class="my-4">
        <h2>Hey!</h2>
        <p>
            You're signed in as <strong>{$user.email}</strong>.
        </p>
        <button class="mt-2" onclick={signOut}>Sign out</button>
    </div>
{:else}
    <div class="flex justify-center my-4">
        <a href="/login" class="btn">Login / Sign Up</a>
    </div>
{/if}