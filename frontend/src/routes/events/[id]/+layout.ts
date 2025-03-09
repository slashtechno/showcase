// https://svelte.dev/docs/kit/load#Layout-data
import { error, isHttpError, redirect } from "@sveltejs/kit";
import type { LayoutLoad } from "./$types";
import { user } from "$lib/user.svelte";
import { client } from "$lib/client/sdk.gen";
import { EventsService } from "$lib/client/sdk.gen";
import { page } from "$app/state";
import type { Event } from "$lib/client";

let partOfEvent = false;

export const load: LayoutLoad = async ({ params, fetch, url, route }) => {
  client.setConfig({ fetch });

  if (!params.id) {
    throw error(400, "no id provided");
  }

  let event: { data: Event | null } = {
    data: null,
  };
  try {
    event = await EventsService.getEventEventsEventIdGet({
      path: {
        event_id: params.id,
      },
      throwOnError: true,
    });
    partOfEvent = true;
  } catch (err) {
    // If request fails (user might not be part of the event), load it unauthenticated (right now this is the same response)
    try {
      event =
        await EventsService.getEventUnauthenticatedEventsUnauthenticatedEventIdGet(
          {
            path: {
              event_id: params.id,
            },
            throwOnError: true,
          },
        );
    } catch (err) {
      console.error(err);
      throw error(500, "Failed to load event");
    } 
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
      partOfEvent,
    },
    title: event.data.name,
    meta,
  };
};
