import { api } from '$lib/api/client.svelte';
import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import type { Project } from '$lib/api/types';

export const load: PageLoad = async ({ params }) => {
    const { id } = params;
    try {  
        const leaderboard =  await api.getLeaderboard(id)
        let projects: {project: Project, points: number}[] = []
        for (const project of leaderboard) {
            projects.push({project: await api.getProject(project.id), points: project.points})
        }
        return { projects };
    } catch (err) {
        console.error(err);
        throw error(500, 'Failed to load rankings');
    }
}
