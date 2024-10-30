<script>
    import { currentUser, pb } from "$lib/pocketbase";
    import { onMount } from "svelte";

    let baseURL = '';

    function signOut() {
        pb.authStore.clear();
    }

    onMount(() => {
        baseURL = window.location.origin;
    });
</script>

{#if $currentUser}
    <div class="my-4">
        <h2>Hey!</h2>
        <p>
            You're signed in as {$currentUser.username}.
        </p>
        <button class="mt-2" on:click={signOut}>Sign out</button>
    </div>
{:else}
    <div class="flex justify-center my-4">
        <a href="/login" class="btn">Login / Sign Up</a>
    </div>
    <div class="justify-center my-4">
        <a href="/users/angad">Example profile</a>
    </div>
{/if}
