import type { HTTPValidationError } from "$lib/client/types.gen";
import { toast } from "svelte-sonner";
export function handleError(error: HTTPValidationError | undefined) {
  if (Array.isArray(error?.detail)) {
    const invalidFields = error.detail.map((e) => e.msg);
    toast(invalidFields.join(" | "));
  } else if (typeof error?.detail === "string") {
    toast(error.detail);
  } else {
    console.error(error);
    toast("An error occurred, check the console for more details");
  }
}
