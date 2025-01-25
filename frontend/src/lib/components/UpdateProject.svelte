<script lang="ts">
  import { EventsService, ProjectsService } from "$lib/client/sdk.gen";
  import type { Event, Project } from "$lib/client";
  import { toast } from "svelte-sonner";
  import { handleError } from "$lib/misc";
  import type { ProjectUpdate } from "$lib/client/types.gen";
  import { fade } from "svelte/transition";

  let project: ProjectUpdate = $state({
    name: "",
    readme: "https://example.com",
    repo: "",
    image_url: "",
    description: "",
  });
  let chosenProject: Project = $state({} as Project);
$inspect(chosenProject)
  let projects: Project[] = $state([]);
  let fetchedProjects = false;

  let showDeleteAlert = $state(false);

  async function fetchProjects() {
    try {
      toast("Fetching projects...");
      const { data } = await ProjectsService.getProjectsProjectsMineGet({
        throwOnError: true,
      });
      projects = data;
      fetchedProjects = true;
    } catch (err) {
      handleError(err);
    }
  }

  async function deleteProject() {
    showDeleteAlert = false;
    try {
      await ProjectsService.deleteProjectProjectsProjectIdDelete({
      path: { project_id: chosenProject.id },
        throwOnError: true,
      });
      toast("Project deleted successfully");
      // Reset the fields
      project = {} as ProjectUpdate;
      chosenProject = {} as Project;
      // Fetch the projects again if the user wants to perform another update to reflect the deletion
      fetchedProjects = false;
    } catch (err) {
      handleError(err);
    }
  }

  async function confirmDeleteProject() {
    showDeleteAlert = true;
    setTimeout(() => {
      showDeleteAlert = false;
    }, 5000);
  }

  async function updateProject() {
    try {
      await ProjectsService.updateProjectProjectsProjectIdPut({
        path: { project_id: chosenProject.id },
        body: project,
        throwOnError: true,
      });
      toast("Project updated successfully");
      // Reset the fields
      project = {} as ProjectUpdate;
      chosenProject = {} as Project;
      // fetch the projects again if the user wants to perform another update
      fetchedProjects = false;
    } catch (err) {
      handleError(err);
    }
  }
</script>

<div class="p-4 max-w-md mx-auto">
  {#if showDeleteAlert}
    <div role="alert" class="alert" in:fade out:fade>
      <span>Are you <strong>sure</strong> you want to delete this project?</span
      >
      <div>
        <button class="btn" onclick={() => (showDeleteAlert = false)}
          >Cancel</button
        >
        <button class="btn btn-error" onclick={() => deleteProject()}
          >Delete</button
        >
      </div>
    </div>
  {/if}
  <form onsubmit={updateProject} class="space-y-4">
    <label class="form-control">
      <div class="label">
        <span class="label-text text-primary">Choose a project to update</span>
      </div>
      <select
        bind:value={chosenProject}
        class="select select-bordered"
        onfocus={() => {
          if (!fetchedProjects) fetchProjects();
        }}
        onchange={() => {
          project = { ...chosenProject };
          showDeleteAlert = false;
        }}
      >
        <option value="" disabled selected>Select a project to update</option>
        {#each projects as project}
          <option value={project}>{project.name}</option>
        {/each}
      </select>
    </label>
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
    {#if chosenProject.id}
    <button type="submit" class="btn btn-block mt-4 btn-primary">
      Update Project
    </button>
    <button
    class="btn btn-block mt-4 btn-warning"
    type="button"
    onclick={() => confirmDeleteProject()}
    >
    Delete Project
  </button>
  {/if}
</form>
</div>
