import { api } from '$lib/api/client.svelte';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';


export const load: PageLoad = async ({ params }) => {
    console.debug('Getting event and projects for ranking. Logging to see if this is running on the server or client');
    const { id } = params;
    try {
        const event = await api.getEvent(id);
        const projects = await api.getEventProjects(id);
        return { event, projects };
    } catch (err) {
        console.error(err);
        throw error(500, 'Failed to load event or projects');
    }
}
