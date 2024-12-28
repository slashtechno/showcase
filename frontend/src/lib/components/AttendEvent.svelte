<script lang="ts">
  import { EventsService } from "$lib/client/sdk.gen";
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/apiErrorCheck";
  let joinCode = $state("");

  // Function to create a new event
  async function attendEvent() {
    try {
      await EventsService.attendEventEventsAttendPost({
        query: { join_code: joinCode },
        throwOnError: true,
      });
      toast("Joined event successfully");
      // Reset join code to empty string
      joinCode = "";
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="p-4 max-w-md mx-auto">
  <input
    type="text"
    bind:value={joinCode}
    placeholder="8 character join code"
    class="mb-2 p-2 border rounded w-full"
  />
  <!-- Event description field -->
  <!-- <textarea 
        bind:value={howDidYouHear} 
        placeholder="How did you hear about this event?" 
        class="mb-2 p-2 border rounded w-full" 
    ></textarea> -->

  <button
    onclick={attendEvent}
    class="btn-block btn"
  >
    Join the adventure!
  </button>
</div>
