import type { ServerInit } from '@sveltejs/kit';
import { onMount } from "svelte";
import { api } from "$lib/api/client.svelte";
import { user, signOut, validateToken } from "$lib/user.svelte";

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