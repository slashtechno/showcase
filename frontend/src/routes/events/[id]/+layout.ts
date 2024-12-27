// https://svelte.dev/docs/kit/load#Layout-data
import { error, redirect} from '@sveltejs/kit';
import type { LayoutLoad } from './$types';
import { user } from '$lib/user.svelte';
import {client} from '$lib/client/sdk.gen';
import { EventsService } from '$lib/client/sdk.gen';


export const load: LayoutLoad = async ({ params, fetch }) => {
    client.setConfig({ fetch });
    if (!params.id) {
        throw error(400, 'no id provided');
    }

    if (!user.isAuthenticated) {
        throw error(401, 'Unauthorized, try logging in first');
        // return redirect(302, '/login');
    }

    try {
        const event = await EventsService.getEventEventsEventIdGet({
            path: {
                event_id: params.id
            }
        });

        if (!event.data) {
            throw error(404, 'Event not found');
        }
        const meta = [
            {
                name: 'description',
                content: event.data.description || 'No description provided'
            }
        ]
        return {
            event: {
            ...event.data,
            owned: 'attendees' in event
        },
        title: event.data.name,
        meta
        };
    } catch (err) {
        console.error(err);
        console.debug("Client used to fetch event", client);
        throw error(500, 'Failed to load event');
    }
}