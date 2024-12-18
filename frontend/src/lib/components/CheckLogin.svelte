<svelte:options runes />
<script lang="ts">
    // import { onDestroy, onMount } from "svelte";
    import { api } from "$lib/api/client";
    import {user} from "$lib/stores";
    // import type { Unsubscriber } from "svelte/store";

    // let unsubscribe: Unsubscriber;
    // let tokenVerified = false;

    function signOut() {
        console.log('Signing out (button clicked)');
        // Clear auth state
        user.set({ email: '', token: '' });
        // Remove token from localStorage
        localStorage.removeItem('token');
    }
</script>

{#if $user.email}
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