<script lang="ts">
    import ProjectCard from '$lib/components/ProjectCard.svelte';
    import { onMount } from 'svelte';
    import type { PageData } from './$types';

    let eventId: string;

    let {data}: {data: PageData} = $props();
    let {projects} = data;

</script>

<div class="container mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-4">Leaderboard</h1>
    <ol class="list-decimal list-inside">
        <!-- {#each projects as { project, points }} -->
        {#each projects as project}
            <li class="mb-4">
                <ProjectCard project={project} isSelected={false} toggle={() => {}} selectable={false} />
                <p class="text-gray-600">Points: {project.points}</p>
            </li>
        {/each}
    </ol>
</div>