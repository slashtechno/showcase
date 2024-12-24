<script lang="ts">
    import { onMount } from "svelte";
    import { toast } from "svelte-sonner";

    let { data } = $props();

    console.log(data);
</script>

<div class="text-center">
    <h1 class="text-2xl font-semibold">{data.name}</h1>
    <p class="text-gray-600">{data.description}</p>
    <!-- Link to /events/{data.id}/rank -->
</div>
<div class="flex justify-center">
    <a href={`/events/${data.id}/rank`} class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Rank Projects</a>
</div>
<!-- Leaderboard button -->
<div class="flex justify-center">
    <a href={`/events/${data.id}/leaderboard`} class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Leaderboard</a>
</div>