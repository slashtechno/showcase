<script lang="ts">
    import '../app.css';
    import { Toaster } from 'svelte-sonner';
    import { page } from '$app/state';
    let { children } = $props();
    import { onMount } from 'svelte';
    // import CheckAuth from '$lib/components/CheckAuth.svelte';

    onMount(() => {
        console.debug("Page data:", page.data);
    });
</script>

<svelte:head>
    {#if page.data.title}
        <title>{page.data.title} | Showcase</title>
    {:else}
        <title>Showcase</title>
    {/if}
    {#if page.data.meta}
    {#each page.data.meta as {name, content}}
            <meta name={name} content={content} />
    {/each}
    {:else}
        <meta name="description" content="Showcase" />
    {/if}
</svelte:head>

<nav class="bg-gray-400 p-4 text-center">
    <a href="/" class="text-white text-2xl font-bold">Showcase</a>
</nav>
<!-- <CheckAuth /> -->
{@render children()}
<!-- All pages should be able to show toasts -->
<Toaster />
<!--  Check for auth on all pages -->