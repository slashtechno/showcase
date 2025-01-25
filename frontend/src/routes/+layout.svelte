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

  let showModal = $state(false);
</script>

<svelte:head>
  {#if page.data.title}
    <title>{page.data.title} | Podium</title>
  {:else}
    <title>Podium</title>
  {/if}
  {#if page.data.meta}
    {#each page.data.meta as { name, content }}
      <meta {name} {content} />
    {/each}
  {:else}
    <meta name="description" content="Podium" />
  {/if}
</svelte:head>

<nav class="p-4 text-center bg-neutral">
  <a href="/" class="text-2xl font-bold text-neutral-content">Podium</a>
</nav>
<!--  Check for auth on all pages -->
<!-- <CheckAuth /> -->
{@render children()}

<div class="fixed bottom-4 left-4">
  <!-- Info Button -->
  <button
    class="btn btn-info btn-square btn-sm font-serif font-light"
    aria-label="Info"
    onclick={() => {
      showModal = true;
    }}
  >
    i
  </button>
</div>

<!-- Modal -->
{#if showModal}
  <div class="modal modal-open modal-bottom sm:modal-middle">
    <div class="modal-box">
      <h2 class="font-bold text-lg">About the Project</h2>
      <p class="py-4">
        Podium is <a href="https://hackclub.com">Hack Club's </a><a
          href="https://github.com/hackclub/podium">open-source</a
        >
        peer-judging platform for
        <a href="https://hackathons.hackclub.com/">hackathons</a>. If you
        encounter issues, feel free to
        <a href="https://github.com/hackclub/podium/issues">report</a> them. Need help? Ask on the <a href="https://hackclub.com/slack">Slack</a> or email <a href="mailto:team@hackclub.com">team@hackclub.com</a>.
      </p>
      <p class="text-right">
        <a href="https://github.com/slashtechno">-Angad Behl</a>
      </p>
      <div class="modal-action">
        <button
          class="btn"
          onclick={() => {
            showModal = false;
          }}>Close</button
        >
      </div>
    </div>
  </div>
{/if}

<div class="fixed bottom-4 right-4">
  <ThemeSwitcher />
</div>

<!-- All pages should be able to show toasts -->
<Toaster />

<style>
  .modal-box a {
    @apply underline rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-0.5 underline-offset-2 decoration-accent;
  }
</style>
