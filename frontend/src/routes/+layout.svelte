<script lang="ts">
  import "../app.css";
  import { Toaster } from "svelte-sonner";
  import { navigating, page } from "$app/state";
  let { children } = $props();
  import { onMount } from "svelte";
  import { themeChange } from "theme-change";
  import ThemeSwitcher from "$lib/components/ThemeSwitcher.svelte";
  import { setSystemTheme, returnLoadingText } from "$lib/misc";
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
  {/if}
  {#if page.data.meta}
    {#each page.data.meta as { name, content }}
      <meta {name} {content} />
    {/each}
  {/if}
</svelte:head>

<nav class="p-1 text-center rounded-b-full w-1/2  mx-auto bg-neutral relative max-h-30">
  <a href="/" class="text-2xl font-bold text-neutral-content">Podium</a>
  <div class="grid grid-cols-2 items-center p-2 w-7/12 mx-auto max-h-40 my-auto space-x-2">
   <a href="/projects" class="btn btn-xs ring-1 ring-opacity-45 ring-accent">Projects</a>
   <a href="/events" class="btn btn-xs ring-1 ring-opacity-45 ring-accent">Events</a>
  </div>
</nav>


{#if navigating.to}
  <div class="flex items-center justify-center min-h-screen flex-col">
    <span class="loading loading-ball loading-lg mb-2"></span>
    {returnLoadingText()}
  </div>
{:else}
  {@render children()}
{/if}


<div class="fixed bottom-4 left-4">
  <!-- Info Button -->
  <button
    class="btn btn-info btn-square btn-md font-serif font-light"
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
        <a href="https://github.com/hackclub/podium/issues">report</a> them.
        Need help? Ask on the <a href="https://hackclub.com/slack">Slack</a> or
        email <a href="mailto:team@hackclub.com">team@hackclub.com</a>.
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
    /* @apply underline rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-0.5; */
  }
</style>
