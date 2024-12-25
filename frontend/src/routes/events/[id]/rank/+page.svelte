<svelte:options runes />

<script lang="ts">
    import { toast } from 'svelte-sonner';
    import { api } from '$lib/api/client.svelte';
    import ProjectCard from '$lib/components/ProjectCard.svelte';
    import { onMount } from 'svelte';
    
    let { data } = $props();
    let { event, projects } = data;
    let selectedProjects: string[] = $state([])

    let toSelect = (projects.length >= 20) ? 3 : 2;

    function toggleProjectSelection(projectId: string) {
        if (selectedProjects.includes(projectId)) {
            // If the project is already selected, remove it from the list
            selectedProjects = selectedProjects.filter(id => id !== projectId);
        } else {
            if (selectedProjects.length < 3) {
                // If the project is not selected and the limit is not reached, add it to the list
                selectedProjects = [...selectedProjects, projectId];
            }
        }
    }

    async function submitVote() {
        if (selectedProjects.length < 2 || (projects.length >= 20 && selectedProjects.length < 3)) {
            toast('Please select the required number of projects');
            return;
        }
        try {
            await api.submitVote({ event_id: event.id, projects: selectedProjects });
            toast('Vote submitted successfully');
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        }
    }
</script>

<!-- Basic information about voting -->
<div class="bg-gray-100 p-4 text-center">
    <p class="text-gray-600">Select your top {toSelect} projects in no particular order</p>
</div>

<div class="container mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-4">{event?.name}</h1>
    <p class="text-gray-600 mb-6">{event?.description}</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {#each projects as project}
            <ProjectCard
                project={project}
                isSelected={selectedProjects.includes(project.id)}
                toggle={() => toggleProjectSelection(project.id)}
                selectable={true}
            />
        {/each}
    </div>
    <button class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700" onclick={submitVote}>Submit Vote</button>
</div>