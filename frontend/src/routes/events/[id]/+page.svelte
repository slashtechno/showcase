<script lang="ts">
    import { user } from "$lib/user.svelte";
  import type { PageData } from "./$types";
  let { data }: { data: PageData } = $props();
</script>

<div class="text-center p-4">
  <h1 class="text-2xl font-semibold">{data.event.name}</h1>
  <p class="text-gray-600">{data.event.description}</p>
  <!-- Link to /events/{data.id}/rank -->
</div>
<div class="flex justify-center flex-col mx-auto max-w-md space-y-4 mt-4">
  {#if user.isAuthenticated}
  <a href={`/events/${data.event.id}/rank`} class="btn-primary btn"
    >Rank Projects</a
  >
  {/if}
  <a href={`/events/${data.event.id}/leaderboard`} class="btn-primary btn"
    >Leaderboard</a
  >
</div>
