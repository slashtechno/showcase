<script lang="ts">
    import ProjectCard from '$lib/components/ProjectCard.svelte';
    import { onMount } from 'svelte';

    let eventId: string;

    let { data } = $props();
    let {projects} = data;
    onMount(() => {
        console.log(data);
    });
</script>

<div class="container mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-4">Leaderboard</h1>
    <ol class="list-decimal list-inside">
        {#each projects as { project, points }}
            <li class="mb-4">
                <ProjectCard project={project} isSelected={false} toggle={() => {}} selectable={false} />
                <p class="text-gray-600">Points: {points}</p>
            </li>
        {/each}
    </ol>
</div>