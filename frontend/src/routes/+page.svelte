<script lang="ts">
    // import CreateProject from '$lib/components/CreateProject.svelte';
    import CheckLogin from '$lib/components/CheckLogin.svelte';
    // import RankProjects from '$lib/components/RankProjects.svelte';

    import { onMount, onDestroy } from "svelte";
    import { api } from "$lib";
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
            user.set({ email: "", token: localStorage.getItem('token')! });
        }

        unsubscribe = user.subscribe((value) => {
            const token = value.token;
            if (token && !tokenVerified) {
                api.verifyAuth(token).then((response) => {
                    console.log('Token is valid');
                    localStorage.setItem('token', token);
                    user.set({ email: response.email, token: token });
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

<div class="space-y-8 p-4">
    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Login</h2>
        <CheckLogin />
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Events</h2>
        <a href="/events" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Events Dashboard
        </a>
    </section>

    <section class="p-4 border rounded-lg shadow-sm">
        <div class="mb-4">
            <h2 class="text-xl font-semibold">Rank Projects</h2>
            <p>Duplicate votes or rankings will result in an error.</p>
        </div>
        <!-- <RankProjects /> -->
    </section>
</div>