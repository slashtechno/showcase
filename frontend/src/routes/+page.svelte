<svelte:options runes />

<script lang="ts">
  import CreateProject from "$lib/components/CreateProject.svelte";
  import AttendEvent from "$lib/components/AttendEvent.svelte";
  import { user, signOut } from "$lib/user.svelte";
    import Page from "./events/+page.svelte";
</script>

<div class="space-y-8 p-4">
  <section class="p-4 border rounded-lg shadow-sm">
    <h2 class="text-xl font-semibold mb-4">Login</h2>
    {#if user.isAuthenticated}
      <div class="my-4 text-center">
        <h2>Hey!</h2>
        <p>
          You're signed in as <strong>{user.email}</strong>.
        </p>
        <button class="btn mt-2" onclick={signOut}>Sign out</button>
      </div>
    {:else}
      <div class="flex justify-center my-4">
        <a href="/login" class="btn">Login / Sign Up</a>
      </div>
    {/if}
  </section>

  {#if user.isAuthenticated}
    <!-- Style and center -->
    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Events</h2>
      <div class="flex justify-center">
      <a href="/events" class="btn btn-wide btn-primary"> Events Dashboard </a>
    </div>
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Create Project</h2>
      <CreateProject />
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Attend Event</h2>
      <AttendEvent />
    </section>
    <div class="flex justify-center">
    <a class="btn btn-wide btn-primary" href="/projects">Update my projects</a>
    <!-- <a class="btn btn-block btn-primary" href="/projects">Update my projects</a> -->
  </div>
  {/if}
</div>
