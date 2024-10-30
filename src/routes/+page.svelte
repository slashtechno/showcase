<script>
    import CreateProject from '$lib/components/CreateProject.svelte';
    import CreateEvent from '$lib/components/CreateEvent.svelte';
    import CheckLogin from '$lib/components/CheckLogin.svelte';
</script>

<div>
    <CheckLogin />
    <CreateEvent />
    <!-- Add space between the components -->
    <div class="my-4"></div>
    <CreateProject />
</div>