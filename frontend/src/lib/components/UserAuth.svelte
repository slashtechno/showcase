<script>
    import { ApiClient } from '$lib/api/client';
    import { toast, Toaster } from "svelte-sonner";
    import { onMount } from "svelte";
    import { user } from "$lib/stores";

    // rest is the extra props passed to the component
    let { ...rest } = $props();

    let isLoading = $state(false);
    let email = $state('');
    const apiClient = new ApiClient();

    // Function to handle login
    async function login() {
        isLoading = true;
        try {
            // Request magic link for the provided email
            const response = await apiClient.requestLogin(email);
            toast(`Magic link sent to ${email}`);
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        } finally {
            isLoading = false;
        }
    }

    // Function to handle verification link
    async function verifyToken(token) {
        isLoading = true;
        try {
            const response = await apiClient.verifyToken(token);
            // Might be good to make the token verification also return the email
            user.set({token: response.access_token });
            // Store the token in localStorage
            localStorage.setItem('token', response.access_token);
            toast('Login successful');
        } catch (err) {
            console.error(err);
            toast(JSON.stringify(err));
        } finally {
            isLoading = false;
        }
    }

    // Check for token in URL on mount
    // For example: /login?token=abc123
    onMount(() => {
        const urlParams = new URLSearchParams(window.location.search);
        const token = urlParams.get('token');
        if (token) {
            verifyToken(token);
        }
    });

    // Prevent default form submission
    function preventDefault(fn) {
        return function (event) {
            event.preventDefault();
            fn.call(this, event);
        };
    }
</script>


<div class="grid gap-6 max-w-sm mx-auto p-6" {...rest}>
    <div class="text-center">
        <h2 class="text-2xl font-bold mb-2">Welcome</h2>
        <p class="text-gray-600 mb-4">Sign in with your email to continue</p>
    </div>

    <form onsubmit={preventDefault(login)} class="space-y-4">
        <div class="grid gap-2">
            <div class="grid gap-1.5">
                <label class="text-sm font-medium" for="email">
                    Email address
                </label>
                <input
                    id="email"
                    placeholder="name@example.com"
                    type="email"
                    autocomplete="off"
                    disabled={isLoading}
                    bind:value={email}
                    class="w-full px-3 py-2 border rounded-md"
                />
                <p class="text-sm text-gray-500">
                    We'll send you a magic link to sign in
                </p>
            </div>
            <div class="flex justify-center mt-4">
                <button
                    type="button"
                    onclick={login}
                    disabled={isLoading}
                    class="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700"
                >
                    {#if isLoading}
                        <span class="loader mr-2"></span>
                    {/if}
                    Sign In with Email
                </button>
            </div>
        </div>
    </form>

    <div class="text-center mt-4">
        <a href="/" class="text-sm text-blue-600 hover:text-blue-800">← Back to Home</a>
    </div>
</div>
