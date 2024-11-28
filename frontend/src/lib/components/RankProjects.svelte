<script>
    import { pb } from '$lib/pocketbase';
    import { toast } from 'svelte-sonner';
    import { currentUser } from '$lib/pocketbase';
    import { onMount } from 'svelte';

    let events = $state([]);
    let selectedEvent = $state('');
    let projects = $state([]);
    let rankings = $state([]);

    // Fetch events on component mount
    onMount(fetchEvents);

    async function fetchEvents() {
        try {
            events = await pb.collection('events').getFullList();
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
            projects = await pb.collection('projects').getFullList({
                filter: `event = "${selectedEvent}"`
            });
            rankings = projects.map(() => null);
        } catch (error) {
            console.error('Error fetching projects:', error);
            toast.error('Failed to load projects.');
        }
    }

    async function submitVotes() {
        // https://svelte.dev/docs/svelte/v5-migration-guide#Event-changes-Event-modifiers
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
            await Promise.all(
                projects.map((project, index) => {
                    return pb.collection('votes').create({
                        user: $currentUser.id,
                        project: project.id,
                        event: selectedEvent,
                        ranking: parseInt(rankings[index])
                    });
                })
            );
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
                <!-- <input type="number" min="1" max={projects.length} bind:value={rankings[index]} /> -->
                <input type="number" min="1" max={projects.length} bind:value={rankings[index]} class="w-16 p-2 border rounded-lg text-center" />
            </div>
        {/each}
        <button type="submit">Submit Rankings</button>
    </form>
{/if}