import type { ServerInit } from '@sveltejs/kit';
import { client } from '$lib/client/sdk.gen';
import { user, signOut, validateToken } from "$lib/user.svelte";
// @ts-ignore
import { PUBLIC_API_URL } from '$env/static/public'

client.setConfig(
	{
		baseUrl: PUBLIC_API_URL,
		headers: {
			'Authorization': `Bearer ${user.token}`
		}
	}
);
export const init: ServerInit = async () => {
	if (user.isAuthenticated) {
		console.debug('User is already authenticated, checking token');
		validateToken(user.token);
		console.log('Finished auth');
		return;
	}

	const token = localStorage.getItem('token');
	if (token) {
		console.debug('Token found in localStorage', token);
		await validateToken(token);
		console.log('Finished auth');
	} else {
		console.debug('No token found in localStorage');
	}

};