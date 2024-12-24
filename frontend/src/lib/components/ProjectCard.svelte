<script lang="ts">
    import type { Project } from '$lib/api/types';
    export let project: Project;
    export let isSelected: boolean;
    export let toggle: () => void;
    export let selectable: boolean = false;
</script>

<button
    type="button"
    class="project-card border p-4 rounded cursor-pointer {isSelected ? 'border-blue-500' : 'border-gray-300'}"
    onclick={selectable ? toggle : null}
    onkeydown={selectable ? (e) => e.key === 'Enter' && toggle() : null}
    aria-pressed={isSelected}
    disabled={!selectable}
>
    <img src="https://lorempic.com/640/480" alt="Project" class="w-full h-32 object-cover mb-4" />
    <h2 class="text-lg font-semibold">{project.name}</h2>
    <p class="text-gray-600">{project.description}</p>
</button>
