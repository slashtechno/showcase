<script>
    import { pb } from '$lib/pocketbase';
    import { toast } from 'svelte-sonner';
    import { onMount } from 'svelte';
    import { currentUser } from '$lib/pocketbase';
    let projectName = '';
    let events = [];
    let selectedEvent = '';

    async function fetchEvents() {
        try {
            const fetchedEvents = await pb.collection('events').getFullList();
            events = fetchedEvents;
        } catch (error) {
            console.error('Error fetching events:', error);
            toast.error('Failed to load events.');
        }
    }

    onMount(() => {
        fetchEvents();
    });

    async function createProject() {
        try {
            const data = {
                name: projectName,
                event: selectedEvent,
                owner: $currentUser.id // Include the owner's ID
            };
            await pb.collection('projects').create(data);
            toast.success('Project created successfully!');
            projectName = ''; // Reset the input field
            selectedEvent = ''; // Reset the event selection
        } catch (error) {
            console.error('Error creating project:', error);
            toast.error('Failed to create project: ' + error.message);
        }
    }
</script>

<input type="text" bind:value={projectName} placeholder="Enter project name" />

<select bind:value={selectedEvent} onfocus={fetchEvents}>
    <option value="" disabled selected>Select an event</option>
    {#each events as event}
        <option value={event.id}>{event.name}</option>
    {/each}
</select>

<button onclick={createProject}>Create Project</button>
