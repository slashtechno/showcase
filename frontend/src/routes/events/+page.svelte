<svelte:options runes />

<script lang="ts">
  import AttendEvent from "$lib/components/AttendEvent.svelte";
  import CreateEvent from "$lib/components/CreateEvent.svelte";
  import { EventsService } from "$lib/client";
  import type { PageData } from "./$types";
  import { handleError } from "$lib/misc";

  let { data }: { data: PageData } = $props();

  async function onVotableCheck(value: boolean, eventId: string) {
    try {
      console.log(value, eventId);
      await EventsService.makeVotableEventsMakeVotablePost({
        query: { votable: value, event_id: eventId },
        throwOnError: true,
      });
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="space-y-8 p-4">
  <section>
    <h2 class="text-xl font-semibold mb-4">Create Event</h2>
    <CreateEvent />
  </section>
  <section>
    <h2>Events you own</h2>
    <div class="overflow-x-auto">
    <table class="table w-full table-zebra">
      <thead>
        <tr>
          <th>Event Name</th>
          <th>Description</th>
          <th>Join Code</th>
          <th>Votable</th>
        </tr>
      </thead>
      <tbody>
        {#each data.events.owned_events as event}
          <tr>
            <td><a href={`/events/${event.id}`}>{event.name}</a></td>
            <td>{event.description}</td>
            <!-- <span class="ml-4 bg-base-300 p-1 rounded"></span> -->
            <td
              ><a
                href={`/events/?join_code=${event.join_code}`}
                data-sveltekit-noscroll>{event.join_code}</a
              ></td
            >
            <td
              ><input
                type="checkbox"
                class="checkbox"
                checked={event.votable}
                onchange={(e) =>
                  onVotableCheck(
                    (e.target as HTMLInputElement).checked,
                    event.id,
                  )}
              /></td
            >
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
  </section>
  <section>
    <h2>Events you are attending</h2>
    <div class="overflow-x-auto">
    <table class="table w-full table-zebra">
      <thead>
        <tr>
          <th>Event Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
        {#each data.events.attending_events as event}
          <tr>
            <td><a href={`/events/${event.id}`}>{event.name}</a></td>
            <td>{event.description}</td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
  </section>
  <section>
    <h2 class="text-xl font-semibold mb-4">Attend Event</h2>
    <AttendEvent />
  </section>
</div>

<style>
  a {
    @apply underline rounded transition-colors duration-300 hover:bg-primary hover:text-primary-content p-1 underline-offset-2 decoration-accent;
  }
  section {
    @apply p-6 rounded-lg shadow-sm border-accent border-2 border-dotted border-opacity-50;
  }
</style>
