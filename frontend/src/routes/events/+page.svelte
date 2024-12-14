<svelte:options runes />

<script lang="ts">
    import CreateEvent from "$lib/components/CreateEvent.svelte";

</script>


<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Create Event</h2>
        <CreateEvent />
    </section>
</div>