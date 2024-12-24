import { api } from '$lib/api/client.svelte';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ params }) => {
    const { id } = params;
    try {  
        return {
            projects: await api.getLeaderboard(id),
        }
    } catch (err) {
        console.error(err);
        throw error(500, 'Failed to load rankings');
    }
}
