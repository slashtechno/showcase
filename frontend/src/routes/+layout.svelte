<script lang="ts">
  import "../app.css";
  import { Toaster } from "svelte-sonner";
  import { page } from "$app/state";
  let { children } = $props();
  import { onMount } from "svelte";
  import { themeChange } from "theme-change";
  import ThemeSwitcher from "$lib/components/ThemeSwitcher.svelte";
  import { setSystemTheme } from "$lib/misc";
  // import CheckAuth from '$lib/components/CheckAuth.svelte';

  onMount(() => {
    console.debug("Page data:", page.data);
    themeChange(false);

    setSystemTheme();

  });
</script>

<svelte:head>
  {#if page.data.title}
    <title>{page.data.title} | Showcase</title>
  {:else}
    <title>Showcase</title>
  {/if}
  {#if page.data.meta}
    {#each page.data.meta as { name, content }}
      <meta {name} {content} />
    {/each}
  {:else}
    <meta name="description" content="Showcase" />
  {/if}
</svelte:head>

<nav class="p-4 text-center bg-neutral">
  <a href="/" class="text-2xl font-bold text-neutral-content">Showcase</a>
</nav>
<!--  Check for auth on all pages -->
<!-- <CheckAuth /> -->
{@render children()}

<div class="fixed bottom-4 right-4">
  <ThemeSwitcher />
</div>

<!-- All pages should be able to show toasts -->
<Toaster />
