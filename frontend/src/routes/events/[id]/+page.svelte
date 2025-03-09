<script lang="ts">
    import { user } from "$lib/user.svelte";
  import type { PageData } from "./$types";
  let { data }: { data: PageData } = $props();
</script>

<div class="flex justify-center flex-col mx-auto max-w-md space-y-4 mt-4">
  {#if data.event.partOfEvent}
  <a href={`/events/${data.event.id}/rank`} class="btn-primary btn"
    >Rank Projects</a
  >
  {/if}
  <a href={`/events/${data.event.id}/leaderboard`} class="btn-primary btn"
    >Leaderboard</a
  >
</div>
