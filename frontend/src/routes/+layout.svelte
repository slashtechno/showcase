<script>
	import '../app.css';
	import { Toaster } from 'svelte-sonner';
	let { children } = $props();
	
</script>

<nav class="bg-gray-400 p-4 text-center">
	<a href="/" class="text-white text-2xl font-bold">Showcase</a>
  </nav>
{@render children()}
<!-- All pages should be able to show toasts -->
<Toaster />