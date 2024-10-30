<script>
    import { pb } from '$lib/pocketbase';
    import { toast, Toaster } from "svelte-sonner";

    let isLoading = false;
    let username = '';
    let password = '';

    async function login() {
        isLoading = true;
        try {
            await pb.collection("users").authWithPassword(username, password);
            window.history.back();
        } catch (err) {
            console.error(err.data);
            toast(JSON.stringify(err.data));
        } finally {
            isLoading = false;
        }
    }

    async function signUp() {
        isLoading = true;
        try {
            const data = {
                username,
                password,
                passwordConfirm: password,
            };
            await pb.collection("users").create(data);
            await login();
        } catch (err) {
            console.error(err.data);
            toast(JSON.stringify(err.data));
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="grid gap-6" {...$$restProps}>
    <form on:submit|preventDefault={login}>
        <div class="grid gap-2">
            <div class="grid gap-1">
                <label class="sr-only" for="username">Username</label>
                <input
                    id="username"
                    placeholder="Username"
                    type="text"
                    autocomplete="off"
                    disabled={isLoading}
                    bind:value={username}
                />
                <label class="sr-only" for="password">Password</label>
                <input
                    id="password"
                    placeholder="Password"
                    type="password"
                    autocomplete="off"
                    disabled={isLoading}
                    bind:value={password}
                />
            </div>
            <div class="flex justify-center">
                <button
                    type="button"
                    on:click={login}
                    disabled={isLoading}
                    class="mx-2"
                >
                    {#if isLoading}
                        <span class="loader mr-2"></span>
                    {/if}
                    Sign In
                </button>
                <button
                    type="button"
                    on:click={signUp}
                    disabled={isLoading}
                    class="mx-2"
                >
                    <!-- {#if isLoading}
                    {/if} -->
                    Sign Up
                </button>
            </div>
        </div>
    </form>
</div>
<Toaster />
