<!-- TODO: Migrate to new API -->
<script lang="ts">
  import { toast, Toaster } from "svelte-sonner";
  import { onMount } from "svelte";
  import { user, validateToken } from "$lib/user.svelte";
  import { AuthService, UsersService } from "$lib/client/sdk.gen";
  import type { HTTPValidationError } from "$lib/client/types.gen";
  import { handleError } from "$lib/apiErrorCheck";

  // rest is the extra props passed to the component
  let { ...rest } = $props();

  let isLoading = $state(false);
  let showSignupFields = $state(false);
  // let showSignupFields = $state(true); // ONLY FOR DEBUGGING
  // TODO: consolidate these into a single object
  let email = $state("");
  let first_name = $state("");
  let last_name = $state("");
  let mailing_address = $state("");

  // Function to handle login
  async function login() {
    isLoading = true;
    // Even though error handling is done in the API, the try-finally block is used to ensure the loading state is reset
    try {
      const { data, error } = await UsersService.userExistsUsersExistsGet({
        query: { email },
        throwOnError: false,
      });
      if (data?.exists) {
        // Request magic link for the provided email if the user exists
        await AuthService.requestLoginRequestLoginPost({
          body: { email },
        });
        toast(`Magic link sent to ${email}`);
        // Clear field
        email = "";
      } else if (error) {
        handleError(error);
      } else {
        toast("You don't exist (yet)! Let's change that.");
        showSignupFields = true;
      }
    } finally {
      isLoading = false;
    }
  }

  // Function to handle signup and login
  async function signupAndLogin() {
    isLoading = true;
    try {
      const userPayload = {
        email,
        first_name,
        last_name,
        mailing_address,
      };
      await UsersService.createUserUsersPost({
        body: userPayload,
        throwOnError: true,
      });
      toast(`Magic link sent to ${email}`);
      // Clear values
      email = "";
      first_name = "";
      last_name = "";
      mailing_address = "";
    } finally {
      isLoading = false;
    }
  }

  // Function to handle verification link
  async function verifyMagicLink(token: string) {
    isLoading = true;
    try {
      // AuthService.verifyTokenVerifyGet({query: {token}} as VerifyTokenVerifyGetData).then((response) => {
      const { data, error } = await AuthService.verifyTokenVerifyGet({
        query: { token },
        throwOnError: false,
      });
      if (error) {
        handleError(error);
      } else {
        // Store the token in localStorage
        localStorage.setItem("token", data.access_token);
        // console.log('Token passed, set, and verified successfully', response);
        // Just verify the new token since that will store it too. If this isn't valid, there's an issue since that means the server is returning a bad token.
        await validateToken(data.access_token);
        toast("Login successful");
      }
    } finally {
      isLoading = false;
    }
  }

  // Check for token in URL on mount
  // For example: /login?token=abc123
  onMount(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get("token");
    if (token) {
      console.log("Token found in URL:", token);
      verifyMagicLink(token);
    }
  });

  // Prevent default form submission (not needed it seems)
  // https://svelte.dev/docs/svelte/svelte-legacy#preventDefault
  // https://svelte.dev/docs/svelte/v5-migration-guide#Breaking-changes-in-runes-mode-Touch-and-wheel-events-are-passive
  // function preventDefault(fn) {
  //     return function (event) {
  //         event.preventDefault();
  //         fn.call(this, event);
  //     };
  // }
</script>

<div class="grid gap-6 max-w-sm mx-auto p-6" {...rest}>
  {#if user.isAuthenticated}
    <div class="text-center">
      <h2 class="text-2xl font-bold mb-2">
        You are logged in as {user.email}
      </h2>
      <button
        class="mt-4 px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700"
        onclick={() => history.back()}
      >
        Go back to previous page
      </button>
    </div>
  {:else}
  <form onsubmit={login} class="space-y-4">
    <div class="form-control">
      <label for="email" class="label">
        <span class="label-text">Email</span>
      </label>
      <input
        id="email"
        type="email"
        class="input input-bordered grow"
        bind:value={email}
        placeholder="example@example.com"
      />
      <label class="label" for="email">
        <span class="label-text-alt">We'll send you a magic link</span>
      </label>
    </div>
  
    {#if showSignupFields}
      <div class="form-control">
        <label for="first_name" class="label">
          <span class="label-text">First Name</span>
        </label>
        <input
          id="first_name"
          type="text"
          class="input input-bordered grow"
          placeholder="Abc"
          bind:value={first_name}
        />
      </div>
  
      <div class="form-control">
        <label for="last_name" class="label">
          <span class="label-text">Last Name</span>
        </label>
        <input
          id="last_name"
          type="text"
          class="input input-bordered grow"
          placeholder="Xyz"
          bind:value={last_name}
        />
      </div>
  
      <div class="form-control">
        <label for="mailing_address" class="label">
          <span class="label-text">Mailing Address</span>
        </label>
        <input
          id="mailing_address"
          type="text"
          class="input input-bordered grow"
          placeholder="1234 Elm St, Springfield, IL 62701"
          bind:value={mailing_address}
        />
      </div>
    {/if}
    <div class="flex justify-center">
      <button
        type="submit"
        class="btn btn-primary"
        disabled={isLoading}
      > Sign in || Sign up </button>
    </div>
  </form>
  
  {/if}
  <div class="text-center mt-4">
    <a href="/" class="text-sm text-blue-600 hover:text-blue-800"
      >← Back to Home</a
    >
  </div>
</div>
