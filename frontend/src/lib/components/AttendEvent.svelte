<script lang="ts">
  import { EventsService } from "$lib/client/sdk.gen";
  import { toast } from "svelte-sonner";
  import { handleError, invalidateEvents } from "$lib/misc";
  import type { AttendEventEventsAttendPostData } from "$lib/client";
  import { afterNavigate, goto, invalidate } from "$app/navigation";
  import { onMount } from "svelte";
  let toSend: AttendEventEventsAttendPostData = $state({
    query: { join_code: "", referral: "" },
  });

  async function attendEvent() {
    try {
      await EventsService.attendEventEventsAttendPost({
        ...toSend,
        throwOnError: true,
      });
      toast("Joined event successfully");
      invalidateEvents();
      // Reset
      toSend.query.join_code = "";
      toSend.query.referral = "";
    } catch (err) {
      handleError(err);
    }
  }

  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const join_code = urlParams.get("join_code");
    if (join_code) {
      toSend.query.join_code = join_code;
      toSend.query.referral = urlParams.get("referral") ?? "Joined from link";
      attendEvent();
      // Clear the query param
      const url = new URL(window.location.href);
      url.searchParams.delete("join_code");
      goto(url.toString(), { replaceState: true, noScroll: true });
    }
  });
</script>

<div class="p-4 max-w-md mx-auto">
  <form onsubmit={attendEvent} class="space-y-4">
    <label class="form-control">
      <div class="label">Join Code</div>
      <input
        type="text"
        bind:value={toSend.query.join_code}
        placeholder="~4 character case-insensitive join code"
        class="w-full input input-bordered"
      />
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">How did you hear about this event?</span>
        <span class="label-text-alt">Optional</span>
      </div>
      <input
        type="text"
        class="input input-bordered grow"
        placeholder="Friend, social media, etc."
        bind:value={toSend.query.referral}
      />
    </label>
    <button type="submit" class="btn-block btn btn-primary">
      Join the adventure!
    </button>
  </form>
</div>
