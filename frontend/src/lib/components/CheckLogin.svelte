<script lang="js">
    import { onMount } from "svelte";
    import {ApiClient} from "$lib/api/client";
    import { user } from '$lib/stores';

    const apiClient = new ApiClient();

    function signOut() {
        // Clear token from API client
        apiClient.token = null;
        // Clear auth state
        user.set({ email: null, token: null });
        // Remove token from localStorage
        localStorage.removeItem('token');
    }

    onMount(() => {
        // Check for existing token in localStorage
        const savedToken = localStorage.getItem('token');
        if (savedToken) {
            // At the moment, /verify is for converting a magic link but /protected-route can be used for verifying a token
                        
            apiClient.verifyAuth(savedToken).then((response) => {
                user.set({token: savedToken, email: response.email});
                console.log('User is signed in');
            }).catch((err) => {
                console.log('Token is invalid', err);
                signOut();
            });
        } else {
            console.log('No token found');
        }
    });
</script>

{#if $user.token}
    <div class="my-4">
        <h2>Hey!</h2>
        <p>
            You're signed in as <strong>{$user.email}</strong>.
        </p>
        <button class="mt-2" on:click={signOut}>Sign out</button>
    </div>
{:else}
    <div class="flex justify-center my-4">
        <a href="/login" class="btn">Login / Sign Up</a>
    </div>
{/if}