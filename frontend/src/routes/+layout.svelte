<script lang="ts">
	import '../app.css';
	import { Toaster } from 'svelte-sonner';
	let { children } = $props();
	
    //  ----
	import { onMount, onDestroy } from "svelte";
    import { api, ApiClient } from "$lib/api/client";
    import { user } from "$lib/stores";
    import type { Unsubscriber } from "svelte/store";

    let unsubscribe: Unsubscriber;
    let tokenVerified = false;

    function signOut() {
        console.log('Signing out');
        user.set({ email: '', token: '' });
        localStorage.removeItem('token');
    }

    onMount(() => {
        if (localStorage.getItem('token')) {
            console.debug('Token found in localStorage, setting user in store');
            user.set({ email: "", token: localStorage.getItem('token')! });
        }

        unsubscribe = user.subscribe((value) => {
            const token = value.token;
            if (api.tokenSet && !tokenVerified) {
                api.verifyAuth().then((response) => {
                    localStorage.setItem('token', token);
                    user.set({ email: response.email, token: token });
                    console.debug('Token verified, setting user in store', token);
                    tokenVerified = true;
                }).catch((err) => {
                    console.log('Token is invalid', err);
                    signOut();
                });
            } else if (!token) {
                console.log('No token found');
            }
        });
    });

    onDestroy(() => {
        if (unsubscribe) {
            console.debug('Unsubscribing from user store');
            unsubscribe();
        }
    });
</script>

<nav class="bg-gray-400 p-4 text-center">
	<a href="/" class="text-white text-2xl font-bold">Showcase</a>
  </nav>
{@render children()}
<!-- All pages should be able to show toasts -->
<Toaster />