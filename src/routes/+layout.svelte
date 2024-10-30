<script>
	import '../app.css';
	import { Toaster } from 'svelte-sonner';
	let { children } = $props();
</script>

{@render children()}
<!-- All pages should be able to show toasts -->
<Toaster />