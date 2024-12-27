<script lang="ts">
    import { api } from "$lib/api/client.svelte";
    import {client} from "$lib/client/sdk.gen";
    import { toast } from 'svelte-sonner';
    let joinCode = $state('');

    // Function to create a new event
    async function attendEvent() {
        try {
            await api.attendEvent(joinCode);
            toast('Joined event successfully');
            // Reset join code to empty string
            joinCode = '';
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        }
    }
</script>

<div class="p-4 max-w-md mx-auto">
    <input 
        type="text" 
        bind:value={joinCode} 
        placeholder="8 character join code" 
        class="mb-2 p-2 border rounded w-full" 
    />
    <!-- Event description field -->
    <!-- <textarea 
        bind:value={howDidYouHear} 
        placeholder="How did you hear about this event?" 
        class="mb-2 p-2 border rounded w-full" 
    ></textarea> -->

    <button 
        onclick={attendEvent}
        class="p-2 bg-blue-500 text-white rounded w-full"
    >
        Join the adventure!
    </button>
</div>