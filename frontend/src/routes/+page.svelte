<script lang="ts">
    import CreateProject from '$lib/components/CreateProject.svelte';
    import CheckLogin from '$lib/components/CheckLogin.svelte';
    // import RankProjects from '$lib/components/RankProjects.svelte';
</script>

<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Login</h2>
        <CheckLogin />
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Events</h2>
        <a href="/events" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Events Dashboard
        </a>
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <div class="mb-4">
            <h2 class="text-xl font-semibold">Rank Projects</h2>
            <p>Duplicate votes or rankings will result in an error.</p>
        </div>
        <!-- <RankProjects /> -->
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Create Project</h2>
        <CreateProject />
    </section>
</div>