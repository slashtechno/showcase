// https://svelte.dev/docs/kit/load#Layout-data
import { error, redirect } from "@sveltejs/kit";
import type { PageLoad } from "./$types";
import { user } from "$lib/user.svelte";
import { client } from "$lib/client/sdk.gen";
import { EventsService } from "$lib/client/sdk.gen";
import { handleError } from "$lib/misc";

export const load: PageLoad = async ({ params, fetch }) => {
  client.setConfig({ fetch });
  if (!user.isAuthenticated) {
    throw error(401, "Unauthorized, try logging in first");
  }

  try {
    const { data } = await EventsService.getAttendingEventsEventsGet({
        throwOnError: true,
      });
    return {
        events: data,
    };
  } catch (err) {
    console.error(err);
    throw error(500, "Failed to load events");
  }
};
