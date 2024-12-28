<svelte:options runes />

<script lang="ts">
  import CreateProject from "$lib/components/CreateProject.svelte";
  import AttendEvent from "$lib/components/AttendEvent.svelte";
  import { user, signOut } from "$lib/user.svelte";
</script>

<div class="space-y-8 p-4">
  <section class="p-4 border rounded-lg shadow-sm">
    <h2 class="text-xl font-semibold mb-4">Login</h2>
    {#if user.isAuthenticated}
      <div class="my-4">
        <h2>Hey!</h2>
        <p>
          You're signed in as <strong>{user.email}</strong>.
        </p>
        <button
          class="btn mt-2"
          onclick={signOut}>Sign out</button
        >
      </div>
    {:else}
      <div class="flex justify-center my-4">
        <a href="/login" class="btn">Login / Sign Up</a>
      </div>
    {/if}
  </section>

  {#if user.isAuthenticated}
    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Events</h2>
      <a
        href="/events"
        class="btn"
      >
        Events Dashboard
      </a>
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Create Project</h2>
      <CreateProject />
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Attend Event</h2>
      <AttendEvent />
    </section>
  {/if}
</div>
