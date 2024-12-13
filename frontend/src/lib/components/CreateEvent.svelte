<script>
    import { ApiClient } from '$lib/api/client';
    import { toast } from 'svelte-sonner';
    let eventName = $state('');
    const apiClient = new ApiClient();

    // Function to create a new event
    async function createEvent() {
        try {
            const event = { name: eventName };
            await apiClient.createEvent(event);
            toast('Event created successfully');
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        }
    }
</script>

<!-- Event name input field -->
<input type="text" bind:value={eventName} placeholder="Enter event name" />
<!-- Create Event button -->
<button onclick={createEvent}>Create Event</button>