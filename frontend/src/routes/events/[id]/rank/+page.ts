import { api } from '$lib/api/client.svelte';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import {client, EventsService} from '$lib/client/sdk.gen';


export const load: PageLoad = async ({ params, fetch }) => {
    client.setConfig({ fetch });
    const { id } = params;
    
    try {
        const projects = await EventsService.getEventProjectsEventsEventIdProjectsGet({
            path: {
                event_id: id
            }
        });
        if (!projects.data) {
            throw error(404, 'No projects found');
        }
        return { projects: projects.data};
    } catch (err) {
        console.error(err);
        throw error(500, 'Failed to load projects');
    }
}
