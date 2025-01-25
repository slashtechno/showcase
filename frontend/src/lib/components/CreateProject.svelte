<script lang="ts">
  import { EventsService, ProjectsService } from "$lib/client/sdk.gen";
  import type { ProjectCreationPayload, Event } from "$lib/client";
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/misc";

  let project: ProjectCreationPayload = $state({
    name: "",
    readme: "https://example.com",
    repo: "",
    demo: "",
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
      project = {
        name: "",
        readme: "https://example.com",
        repo: "",
        demo: "",
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
  <form onsubmit={createProject} class="space-y-4">
    <label class="form-control">
      <div class="label">
        <span class="label-text">Project Name</span>
      </div>
      <input
        type="text"
        bind:value={project.name}
        placeholder="A really cool project!"
        class="input input-bordered grow"
      />
    </label>
    <!-- Project description field -->
    <label class="form-control">
      <div class="label">
        <span class="label-text">Project Description</span>
      </div>
      <textarea
        bind:value={project.description}
        placeholder="Some cool description"
        class="textarea textarea-bordered grow"
      ></textarea>
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">Image URL</span>
        <span class="label-text-alt">
          (such as a raw GitHub link or a #cdn link)</span
        >
      </div>
      <input
        type="text"
        bind:value={project.image_url}
        placeholder="Image URL"
        class="input input-bordered grow"
      />
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">Demo URL</span>
        <span class="label-text-alt"> (a link to an interactive demo)</span>
      </div>
      <input
        type="text"
        bind:value={project.demo}
        placeholder="Demo URL"
        class="input input-bordered grow"
      />
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">Repository URL</span>
        <span class="label-text-alt"> (such as a GitHub link)</span>
      </div>
      <input
        type="text"
        bind:value={project.repo}
        placeholder="Repository URL"
        class="input input-bordered grow"
      />
    </label>
    <label class="form-control">
      <div class="label">
        <span class="label-text">Event</span>
      </div>
      <select
        bind:value={project.event[0]}
        class="select select-bordered"
        onfocus={() => {
          if (!fetchedEvents) fetchEvents();
        }}
      >
        <option value="" disabled selected>Select an event</option>
        {#each events as event}
          <option value={event.id}>{event.name}</option>
        {/each}
      </select>
    </label>
    <button type="submit" class="btn btn-block mt-4"> Create Project </button>
  </form>
</div>
