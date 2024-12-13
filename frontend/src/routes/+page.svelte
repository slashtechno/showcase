<script>
    import CreateProject from '$lib/components/CreateProject.svelte';
    import CreateEvent from '$lib/components/CreateEvent.svelte';
    import CheckLogin from '$lib/components/CheckLogin.svelte';
    import RankProjects from '$lib/components/RankProjects.svelte';
</script>

<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Login</h2>
        <CheckLogin />
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Create Event</h2>
        <CreateEvent />
    </section>

    <!-- <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Create Project</h2>
        <CreateProject />
    </section> -->

    <section class="p-4 border rounded-lg shadow-sm">
        <div class="mb-4">
        <h2 class="text-xl font-semibold">Rank Projects</h2>
        <p>Duplicate votes or rankings will result in an error.</p>
    </div>
        <RankProjects />
    </section>
</div>