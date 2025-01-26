<script lang="ts">
  import UpdateProject from "$lib/components/UpdateProject.svelte";
  import JoinProject from "$lib/components/JoinProject.svelte";
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<div class="p-4 mx-auto space-y-4">
<!-- <div > -->
  <section class="space-y-8 p-4">
    <h2>Your projects</h2>
    <ul>
      {#each data.projects as project}
        <li class="py-2">
          {project.name}
          <span class="ml-4 bg-base-300 p-1 rounded"
            >Join Code: {project.join_code}</span
          >
        </li>
      {/each}
    </ul>
  </section>
  <section>
    <h2 class="text-xl font-semibold mb-4">Join project</h2>
    <JoinProject />
  </section>
  <section>
    <h2 class="text-xl font-semibold mb-4">Update Projects</h2>
    <UpdateProject projects={data.projects} events={data.events}/>
  </section>
</div>

<style>
  section {
    @apply p-6 rounded-lg shadow-sm border-accent border-2 border-dotted border-opacity-50;
  }
</style>
