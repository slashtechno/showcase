import type { HTTPValidationError } from "$lib/client/types.gen";
import { toast } from "svelte-sonner";

type ErrorWithDetail = {
  detail: string;
};

export function handleError(
  error: HTTPValidationError | ErrorWithDetail | Error | unknown,
) {
  // If it's a FastAPI HTTPException, it will have a detail field. Same with validation errors.
  console.error("Error", error);
  if (error && typeof error === "object" && "detail" in error) {
    if (Array.isArray(error?.detail)) {
      // const invalidFields = error.detail.map((e) => e.msg);
      const invalidFields = error.detail.map(
        (e) => `${e.loc.join(".")}: ${e.msg}`,
      );
      toast(invalidFields.join(" | "));
    } else if (typeof error?.detail === "string") {
      toast(error.detail);
    }
  } else {
    // console.error("Unknown error", error);
    if (error instanceof Error) {
      toast(error.message);
    } else {
      toast("An error occurred, check the console for more details");
    }
  }
}
