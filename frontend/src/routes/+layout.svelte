<script lang="ts">
    import '../app.css';
    import { Toaster } from 'svelte-sonner';
    let { children } = $props();
    
    import { initializeAuth } from "$lib/CheckAuth.svelte";

    initializeAuth();
</script>

<nav class="bg-gray-400 p-4 text-center">
    <a href="/" class="text-white text-2xl font-bold">Showcase</a>
</nav>
{@render children()}
<!-- All pages should be able to show toasts -->
<Toaster />