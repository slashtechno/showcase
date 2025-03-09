// https://svelte.dev/docs/kit/load#Layout-data
import { error, isHttpError, redirect } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";
import { user } from "$lib/user.svelte";
import { client } from "$lib/client/sdk.gen";
import { EventsService } from "$lib/client/sdk.gen";
import { page } from "$app/state";
import type { Event } from "$lib/client";

export const load: LayoutLoad = async ({ params, fetch, url, route}) => {
  client.setConfig({ fetch });

  if (!params.id) {
    throw error(400, "no id provided");
  }

  let event: { data: Event | null } = {
    data: null,
  };
  try {
    if (!user.isAuthenticated) {
      // No point checking if they're on something like the rank projects page since it'll error anyway when they try to vote
      // if (url.pathname.endsWith(`/events/${params.id}`)) {
        event =
          await EventsService.getEventUnauthenticatedEventsUnauthenticatedEventIdGet(
            {
              path: {
                event_id: params.id,
              },
              throwOnError: true,
            },
          );
      // } else {
      //   throw error(401, "Unauthorized, try logging in first");
      // }
    } else {
      event = await EventsService.getEventEventsEventIdGet({
        path: {
          event_id: params.id,
        },
        throwOnError: true,
      });
    }
  } catch (err) {

    // If the error was raised above, pass it through
    if (isHttpError(err)) {
      throw err;
    }
    console.error(err);
    throw error(500, "Failed to load event");
  }
    if (!event.data) {
      throw error(404, "Event not found");
    }
    const meta = [
      {
        name: "description",
        content: event.data.description || "No description provided",
      },
    ];
    return {
      event: {
        ...event.data,
        owned: "attendees" in event,
      },
      title: event.data.name,
      meta,
    };
  
};
