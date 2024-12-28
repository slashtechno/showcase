<script lang="ts">
  import { EventsService, ProjectsService } from "$lib/client/sdk.gen";
  import type { ProjectCreationPayload, Event } from "$lib/client";
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/apiErrorCheck";

  let project: ProjectCreationPayload = $state({
    name: "",
    readme: "https://example.com",
    repo: "",
    image_url: "",
    description: "",
    event: [""],
  });
  let events: Event[] = $state([]);
  let fetchedEvents = false;

  // https://svelte.dev/tutorial/svelte/inspecting-state
  // $inspect(project.event).with(console.debug);
  // $inspect(events);
  // $inspect(project)

  async function fetchEvents() {
    try {
      toast("Fetching events; please wait");
      const { data: userEvents } =
        await EventsService.getAttendingEventsEventsGet({ throwOnError: true });
      events = userEvents.attending_events;
      fetchedEvents = true;
    } catch (err) {
      handleError(err);
    }
  }

  async function createProject() {
    try {
      await ProjectsService.createProjectProjectsPost({
        body: project,
        throwOnError: true,
      });
      toast("Project created successfully");
      // Reset the fields
      project = {
        name: "",
        readme: "https://example.com",
        repo: "",
        image_url: "",
        description: "",
        event: [""],
      };
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="p-4 max-w-md mx-auto">
  <!-- Project name input field -->
  <input
    type="text"
    bind:value={project.name}
    placeholder="A really cool project!"
    class="mb-2 p-2 border rounded w-full"
  />
  <!-- Project description field -->
  <textarea
    bind:value={project.description}
    placeholder="Some cool description"
    class="mb-2 p-2 border rounded w-full"
  ></textarea>
  <input
    type="text"
    bind:value={project.image_url}
    placeholder="Image URL (such as a raw GitHub link or a #cdn link)"
    class="mb-2 p-2 border rounded w-full"
  />
  <input
    type="text"
    bind:value={project.repo}
    placeholder="Repository URL (such as a GitHub link)"
    class="mb-2 p-2 border rounded w-full"
  />
  <!-- Dropdown to select event -->
  <select
    bind:value={project.event[0]}
    class="mb-2 p-2 border rounded w-full"
    onfocus={() => {
      if (!fetchedEvents) fetchEvents();
    }}
  >
    <option value="" disabled selected>Select an event</option>
    {#each events as event}
      <option value={event.id}>{event.name}</option>
    {/each}
  </select>
  <button
    onclick={createProject}
    class="p-2 bg-blue-500 text-white rounded w-full"
  >
    Create Project
  </button>
</div>
