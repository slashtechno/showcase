<script lang="ts">
    import { EventsService, ProjectsService } from "$lib/client/sdk.gen";
    import type { Event, Project } from "$lib/client";
    import { toast } from "svelte-sonner";
    import { handleError } from "$lib/misc";
    import type { ProjectUpdate } from "$lib/client/types.gen";
  
    let project: ProjectUpdate = $state({
      name: "",
      readme: "https://example.com",
      repo: "",
      image_url: "",
      description: "",
    });
    let chosenProject: Project = $state({} as Project);

    let projects: Project[] = $state([]);
    let fetchedProjects = false;
  
    async function fetchProjects() {
      try {
        toast("Fetching projects...");
        const { data: userEvents } =
          await ProjectsService.getProjectsProjectsMineGet({
            throwOnError: true,
            });
        fetchedProjects = true;
      } catch (err) {
        handleError(err);
      }
    }
  
    async function updateProject() {
      try {
        await ProjectsService.updateProjectProjectsProjectIdPut({
            path: {}
            body: project,
          throwOnError: true,
        });
        toast("Project updated successfully");
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
          placeholder="Image URL (such as a raw GitHub link or a #cdn link)"
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
          placeholder="Repository URL (such as a GitHub link)"
          class="input input-bordered grow"
        />
      </label>
      <label class="form-control">
        <div class="label">
          <span class="label-text">Event</span>
        </div>
        <select
          bind:value={project.event[0}
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
        <button type="submit" class="btn btn-block mt-4"> Create Project </button>
      </label>
    </form>
  </div>
  