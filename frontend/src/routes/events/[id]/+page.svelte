<script lang="ts">
    import { onMount } from "svelte";
    import { toast } from "svelte-sonner";

    let { data } = $props();

    console.log(data);
</script>

<div class="text-center">
    <h1 class="text-2xl font-semibold">{data.name}</h1>
    <p class="text-gray-600">{data.description}</p>
</div>

