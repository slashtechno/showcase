<!-- <svelte:options runes /> -->
<script lang="ts">
    import { onDestroy, onMount } from "svelte";
    import {api} from "$lib";
    import {user} from "$lib/stores";
    import type { Unsubscriber } from "svelte/store";

    let unsubscribe: Unsubscriber;
    let tokenVerified = false;

    function signOut() {
        // Clear auth state
        user.set({ email: '', token: '' });
        // Remove token from localStorage
        localStorage.removeItem('token');
    }

    onMount(() => {

        // Subscribe to user store
        unsubscribe = user.subscribe((value) => {
            if (value.token && !tokenVerified) {
                // Check if token is valid
                api.verifyAuth(value.token).then((response) => {
                    console.log('Token is valid');
                    localStorage.setItem('token', value.token);
                    user.set({email: response.email, token: value.token});
                    tokenVerified = true;
                }).catch((err) => {
                    console.log('Token is invalid', err);
                    signOut();
                });
            } else {
                console.log('No token found');
            }
        });
    });

    onDestroy(() => {
        // Unsubscribe from user store
        unsubscribe();
    });
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