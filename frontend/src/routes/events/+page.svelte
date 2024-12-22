<svelte:options runes />

<script lang="ts">
    import CreateEvent from "$lib/components/CreateEvent.svelte";
    import { onMount } from "svelte";
    import { api } from "$lib/api/client";
    import type { UserEvents } from "$lib/api/types";
    import { toast } from "svelte-sonner";
    import { goto } from "$app/navigation";

    let events: UserEvents = $state({ owned_events: [], attending_events: [] });

    onMount(async () => {
        try {
            events = await api.getAttendingEvents();
        } catch (error) {
            console.error("Error fetching events:", error);
            toast.error("Failed to load events.");
        }
    });
</script>

<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Create Event</h2>
        <CreateEvent />
    </section>
    <section class="p-4 border rounded-lg shadow-sm">
        <h2>Events you own</h2>
        <ul>
            {#each events.owned_events as event}
                <li class="py-2">
                    <a
                        href={`/events/${event.id}`}
                        class="font-medium text-blue-600 hover:underline"
                        >{event.name}</a
                    >
                    <span class="ml-4 text-gray-600"
                        >Join Code: {event.join_code}</span
                    >
                </li>
            {/each}
        </ul>
    </section>
    <section class="p-4 border rounded-lg shadow-sm">
        <h2>Events you are attending</h2>
        <ul>
            {#each events.attending_events as event}
                <li class="py-2">
                    <a
                        href={`/events/${event.id}`}
                        class="font-medium text-blue-600 hover:underline"
                        >{event.name}</a
                    >
                </li>
            {/each}
        </ul>
    </section>
</div>
