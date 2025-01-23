<script lang="ts">
  import { EventsService } from "$lib/client/sdk.gen";
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/misc";
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
  <form onsubmit={attendEvent} class="space-y-4">
    <label class="form-control">
      <div class="label">Join Code</div>
      <input
        type="text"
        bind:value={joinCode}
        placeholder="8 character join code"
        class="w-full input input-bordered"
      />
    </label>
    <button type="submit" class="btn-block btn"> Join the adventure! </button>
  </form>
</div>
