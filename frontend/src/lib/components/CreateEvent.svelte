<script lang="ts">
  import { handleError } from "$lib/misc";
  import { EventsService } from "$lib/client";
  import { toast } from "svelte-sonner";
    import { invalidate } from "$app/navigation";
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
      invalidate(url => url.pathname.startsWith("/events"));
      // invalidate("events:events")
      // Clear the form
      eventName = "";
      eventDescription = "";
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="p-4 max-w-md mx-auto">
  <form onsubmit={createEvent} class="space-y-2">
    <label class="form-control">
      <div class="label">
        <span class="label-text"> Event name </span>
      </div>
      <input
        type="text"
        bind:value={eventName}
        placeholder="A really cool event"
        class="input input-bordered grow"
      />
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">Event Description</span>
      </div>
      <textarea
        bind:value={eventDescription}
        placeholder="Some cool description"
        class="textarea textarea-bordered grow"
      ></textarea>
    </label>
    <!-- Create Event button -->
    <button class="btn btn-block mt-4" type="submit"> Create Event </button>
  </form>
</div>
