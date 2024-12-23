<svelte:options runes />
<script lang="ts">
    import CreateProject from '$lib/components/CreateProject.svelte';
    import { user, signOut} from '$lib/user.svelte';
    import { onDestroy, onMount } from 'svelte';
    import type { Unsubscriber } from 'svelte/store';

    let unsubscribe: Unsubscriber;

    onMount(() => {
            console.log($state.snapshot(user));
    });
</script>

<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Login</h2>
        {#if user.isAuthenticated}
            <div class="my-4">
                <h2>Hey!</h2>
                <p>
                    You're signed in as <strong>{user.email}</strong>.
                </p>
                <button class="mt-2" onclick={signOut}>Sign out</button>
            </div>
        {:else}
            <div class="flex justify-center my-4">
                <a href="/login" class="btn">Login / Sign Up</a>
            </div>
        {/if}
    </section>

    {#if user.isAuthenticated}
        <section class="p-4 border rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold mb-4">Events</h2>
            <a href="/events" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                Events Dashboard
            </a>
        </section>

        <section class="p-4 border rounded-lg shadow-sm">
            <h2 class="text-xl font-semibold mb-4">Create Project</h2>
            <CreateProject />
        </section>
    {/if}
</div>