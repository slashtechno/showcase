<svelte:options runes />

<script lang="ts">
  import CreateEvent from "$lib/components/CreateEvent.svelte";
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<div class="space-y-8 p-4">
  <section class="p-4 border rounded-lg shadow-sm">
    <h2 class="text-xl font-semibold mb-4">Create Event</h2>
    <CreateEvent />
  </section>
  <section class="p-4 border rounded-lg shadow-sm">
    <h2>Events you own</h2>
    <ul>
      {#each data.events.owned_events as event}
        <li class="py-2">
          <a
            href={`/events/${event.id}`}
            class="font-medium underline hover rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-1"
            >{event.name}</a
          >
          <span class="ml-4 bg-base-300 p-1 rounded"
            >Join Code: {event.join_code}</span
          >
        </li>
      {/each}
    </ul>
  </section>
  <section class="p-4 border rounded-lg shadow-sm">
    <h2>Events you are attending</h2>
    <ul>
      {#each data.events.attending_events as event}
        <li class="py-2">
          <a
            href={`/events/${event.id}`}
            class="font-medium underline hover rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-1"
            >{event.name}</a
          >
        </li>
      {/each}
    </ul>
  </section>
</div>
