import { error, redirect} from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { api } from '$lib/api/client';
import type { Event, OwnedEvent } from '$lib/api/types';

export const load: PageLoad = async ({ params }) => {
    if (!params.id) {
        throw error(400, 'no id provided');
    }

    if (!api.tokenSet) {
        throw error(401, 'Unauthorized');
        // return redirect(302, '/login');
    }

    try {
        const event = await api.getEvent(params.id);
        if (!event) {
            throw error(404, 'Event not found');
        }

        return {
            ...event,
            owned: 'attendees' in event
        };
    } catch (err) {
        console.error(err);
        throw error(500, 'Failed to load event');
    }
}