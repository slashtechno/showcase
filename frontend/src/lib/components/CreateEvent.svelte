<script lang="ts">
    import { api } from "$lib/api/client.svelte";
    import { toast } from 'svelte-sonner';
    // TODO: Use the object instead of individual variables
    let eventName = $state('');
    let eventDescription = $state('');

    // Function to create a new event
    async function createEvent() {
        try {
            // TODO: Add description and other fields
            const event = { name: eventName, description: eventDescription };
            await api.createEvent(event);
            toast('Event created successfully');
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        }
    }
</script>

<div class="p-4 max-w-md mx-auto">
    <!-- Event name input field -->
    <input 
        type="text" 
        bind:value={eventName} 
        placeholder="Enter event name" 
        class="mb-2 p-2 border rounded w-full" 
    />
    <!-- Event description field -->
    <textarea 
        bind:value={eventDescription} 
        placeholder="Enter event description" 
        class="mb-2 p-2 border rounded w-full" 
    ></textarea>
    <!-- Create Event button -->
    <button 
        onclick={createEvent} 
        class="p-2 bg-blue-500 text-white rounded w-full"
    >
        Create Event
    </button>
</div>