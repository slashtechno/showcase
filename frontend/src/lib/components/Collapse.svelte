<script lang="ts">
    import type { Snippet } from "svelte";

  let { title, children }: { title: string, children: Snippet } = $props();
</script>

<button class="collapse bg-base-200 collapse-arrow" >
  <div class="collapse-title text-xl font-medium">
    {title}
  </div>
  <div class="collapse-content">
    {@render children?.()}
</div>
</button>
