<script lang="ts">
  import type { Snippet } from "svelte";

  let { title, children }: { title: string, children: Snippet } = $props();

  function stopPropagation(event: Event) {
    event.stopPropagation();
  }
</script>

<div class="collapse bg-base-200 text-center collapse-arrow">
    <input type="checkbox" />
    <div class="collapse-title text-xl font-medium">{title}</div>
    <div class="collapse-content">
      {@render children?.()}
    </div>
  </div>