<script lang="ts">
	import type { PageData } from './$types';
	let { data }: { data: PageData } = $props();

</script>

<div class="text-center">
    <h1 class="text-2xl font-semibold">{data.event.name}</h1>
    <p class="text-gray-600">{data.event.description}</p>
    <!-- Link to /events/{data.id}/rank -->
</div>
<div class="flex justify-center">
    <a href={`/events/${data.event.id}/rank`} class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Rank Projects</a>
</div>
<!-- Leaderboard button -->
<div class="flex justify-center">
    <a href={`/events/${data.event.id}/leaderboard`} class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">Leaderboard</a>
</div>