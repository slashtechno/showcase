<script>
    import { pb } from '$lib/pocketbase';
    import { toast } from 'svelte-sonner';
    import { currentUser } from '$lib/pocketbase';
    let eventName = '';

    async function createEvent() {
        try {
            const data = {
                name: eventName,
                owner: $currentUser.id // Include the owner's ID
            };
            await pb.collection('events').create(data);
            toast.success('Event created successfully!');
            eventName = ''; // Reset the input field
        } catch (error) {
            console.error('Error creating event:', error);
            toast.error('Failed to create event: ' + error.message);
        }
    }
</script>

<input type="text" bind:value={eventName} placeholder="Enter event name" />
<button onclick={createEvent}>Create Event</button>
