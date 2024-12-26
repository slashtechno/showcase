<script lang="ts">
    import type { Project } from "$lib/client/types.gen";
    interface Props {
        project: Project;
        isSelected: boolean;
        toggle: () => void;
        selectable?: boolean;
    }

    let {
        project,
        isSelected,
        toggle,
        selectable = false
    }: Props = $props();

    // $inspect(project);
</script>

<button
    type="button"
    class="project-card border p-4 rounded-lg shadow-md cursor-pointer transform transition-transform duration-200 hover:scale-105 {isSelected ? 'border-blue-500' : 'border-gray-300'}"
    onclick={selectable ? toggle : null}
    onkeydown={selectable ? (e) => e.key === 'Enter' && toggle() : null}
    aria-pressed={isSelected}
    disabled={!selectable}
>
    <!-- <img src="https://lorempic.com/640/480" alt="Project" class="w-full h-32 object-cover mb-4" /> -->
    <img src={project.image_url} alt="Project" class="w-full h-32 object-contain mb-4" />
    <h2 class="text-lg font-semibold">
        <a href={project.repo} target="_blank" class="text-blue-500 hover:underline">{project.name}</a>
    </h2>
    <p class="text-gray-600">{project.description}</p>
</button>
