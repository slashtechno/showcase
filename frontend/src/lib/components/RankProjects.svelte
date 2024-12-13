<!-- <script>
    import { ApiClient } from '$lib/api/client';
    import { toast } from 'svelte-sonner';
    import { onMount } from 'svelte';

    let events = $state([]);
    let selectedEvent = $state('');
    let projects = $state([]);
    let rankings = $state([]);
    const apiClient = new ApiClient();

    // Fetch events on component mount
    onMount(fetchEvents);

    async function fetchEvents() {
        try {
            events = await apiClient.getEvents();
            console.log($state.snapshot(events));
        } catch (error) {
            console.error('Error fetching events:', error);
            toast.error('Failed to load events.');
        }
    }

    async function fetchProjects() {
        if (!selectedEvent) {
            projects = [];
            rankings = [];
            return;
        }
        try {
            projects = await apiClient.getProjects();
            projects = projects.filter(project => project.event.includes(selectedEvent));
            rankings = projects.map(() => null);
        } catch (error) {
            console.error('Error fetching projects:', error);
            toast.error('Failed to load projects.');
        }
    }

    async function submitVotes(event) {
        // Prevent default form submission
        event.preventDefault();
        const assignedRanks = rankings.filter(rank => rank !== null);
        const uniqueRanks = new Set(assignedRanks);
        if (assignedRanks.length !== uniqueRanks.size) {
            toast.error('Duplicate rankings detected.');
            return;
        }
        if (assignedRanks.length !== projects.length) {
            toast.error('Please rank all projects.');
            return;
        }
        try {
            const vote = {
                event_id: selectedEvent,
                projects: projects.map((project, index) => ({
                    project_id: project.id,
                    ranking: parseInt(rankings[index])
                }))
            };
            await apiClient.submitVote(vote);
            toast.success('Votes submitted successfully!');
        } catch (error) {
            console.error('Error submitting votes:', error);
            toast.error('Failed to submit votes: ' + error.message);
        }
    }
</script>

<select bind:value={selectedEvent} onchange={fetchProjects}>
    <option value="" disabled>Select an event</option>
    {#each events as event}
        <option value={event.id}>{event.name}</option>
    {/each}
</select>

{#if projects.length}
    <form onsubmit={submitVotes}>
        {#each projects as project, index}
            <div>
                <span>{project.name}</span>
                <input type="number" min="1" max={projects.length} bind:value={rankings[index]} class="w-16 p-2 border rounded-lg text-center" />
            </div>
        {/each}
        <button type="submit">Submit Rankings</button>
    </form>
{/if} -->