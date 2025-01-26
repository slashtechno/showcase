<script lang="ts">
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/misc";

  import { ProjectsService } from "$lib/client";
  import type { JoinProjectProjectsJoinPostData } from "$lib/client";

  let toSend: JoinProjectProjectsJoinPostData = $state({
    query: { join_code: "" },
  });

  async function attendEvent() {
    try {
      await ProjectsService.joinProjectProjectsJoinPost({
        ...toSend,
        throwOnError: true,
      });
      toast("Joined project successfully");
      // Reset
      toSend.query.join_code = "";
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
        bind:value={toSend.query.join_code}
        placeholder="~4 character case-insensitive join code"
        class="w-full input input-bordered"
      />
    </label>
    <button type="submit" class="btn-block btn btn-primary">
      Join the development of something great!
    </button>
  </form>
</div>
