<script lang="ts">
  import { handleError } from "$lib/apiErrorCheck";
  import { EventsService } from "$lib/client";
  import { toast } from "svelte-sonner";
  // TODO: Use the object instead of individual variables
  let eventName = $state("");
  let eventDescription = $state("");

  // Function to create a new event
  async function createEvent() {
    try {
      const event = { name: eventName, description: eventDescription };
      await EventsService.createEventEventsPost({
        body: event,
        throwOnError: true,
      });
      toast("Event created successfully");
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="p-4 max-w-md mx-auto">
  <!-- Event name input field -->
  <input
    type="text"
    bind:value={eventName}
    placeholder="Enter event name"
    class="mb-2 p-2 border rounded w-full"
  />
  <!-- Event description field -->
  <textarea
    bind:value={eventDescription}
    placeholder="Enter event description"
    class="mb-2 p-2 border rounded w-full"
  ></textarea>
  <!-- Create Event button -->
  <button
    onclick={createEvent}
    class="p-2 bg-blue-500 text-white rounded w-full"
  >
    Create Event
  </button>
</div>
