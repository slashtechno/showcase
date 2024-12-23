import { api } from '$lib/api/client.svelte';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';


export const load: PageLoad = async ({ params }) => {
    const { id } = params;
    try {
        const event = await api.getEvent(id);
        const projects = await api.getProjects();
        return { event, projects };
    } catch (err) {
        throw error(500, 'Failed to load event or projects');
    }
}
