<script>
    import { pb } from '$lib/pocketbase';
    import { toast } from 'svelte-sonner';
    let projectName = '';

    async function createProject() {
        try {
            const newProject = await pb.collection('projects').create({ name: projectName });
            toast.success('Project created successfully!');
            projectName = ''; // Reset the input field
        } catch (error) {
            console.error('Error creating project:', error);
            toast.error('Failed to create project: ' + error.message);
        }
    }
</script>

<input type="text" bind:value={projectName} placeholder="Enter project name" />
<button on:click={createProject}>Create Project</button>
