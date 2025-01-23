<!-- TODO: Migrate to new API -->
<script lang="ts">
  import { toast, Toaster } from "svelte-sonner";
  import { onMount } from "svelte";
  import { user, validateToken } from "$lib/user.svelte";
  import { AuthService, UsersService } from "$lib/client/sdk.gen";
  import type { HTTPValidationError } from "$lib/client/types.gen";
  import { handleError } from "$lib/misc";
  import type { UserSignupPayload } from "$lib/client/types.gen";

  // rest is the extra props passed to the component
  let { ...rest } = $props();

  let isLoading = $state(false);
  let showSignupFields = $state(false);
  // Consolidate user-related variables into a single object
  let userInfo: UserSignupPayload = $state({
    email: "",
    first_name: "",
    last_name: "",
    street_1: "",
    street_2: "",
    city: "",
    state: "",
    zip_code: "",
    country: "",
  });

  async function eitherLoginOrSignUp() {
    // If showSignupFields is true, the user is signing up and signupAndLogin should be called. Otherwise, the user is logging in and login should be called.
    if (showSignupFields) {
      signupAndLogin();
    } else {
      login();
    }
  }

  // Function to handle login
  async function login() {
    isLoading = true;
    // Even though error handling is done in the API, the try-finally block is used to ensure the loading state is reset
    try {
      const { data, error } = await UsersService.userExistsUsersExistsGet({
        query: { email: userInfo.email },
        throwOnError: false,
      });
      if (data?.exists) {
        // Request magic link for the provided email if the user exists
        await AuthService.requestLoginRequestLoginPost({
          body: { email: userInfo.email },
        });
        toast(`Magic link sent to ${userInfo.email}`);
        // Clear field
        userInfo.email = "";
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
      await UsersService.createUserUsersPost({
        body: userInfo,
        throwOnError: true,
      });
      await login();
      // toast(`Signed up! Check your email for a magic link!`);
      // Clear values
      userInfo = {
        email: "",
        first_name: "",
        last_name: "",
        street_1: "",
        street_2: "",
        city: "",
        state: "",
        zip_code: "",
        country: "",
      };
    } catch (error) {
      handleError(error);
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

<div class="p-4 max-w-md mx-auto" {...rest}>
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
    <!-- space-y-n adds space (margin) between the children -->
    <form onsubmit={eitherLoginOrSignUp} class="space-y-2">
      <label class="form-control">
        <div class="label">
          <span class="label-text">Email</span>
        </div>
        <input
          id="email"
          type="email"
          class="input input-bordered grow"
          bind:value={userInfo.email}
          placeholder="example@example.com"
        />
        <div class="label">
          <span class="label-text-alt"> We'll send you a magic link </span>
        </div>
      </label>

      {#if showSignupFields}
        <label class="form-control">
          <div class="label">
            <span class="label-text">First Name</span>
          </div>
          <input
            id="first_name"
            type="text"
            class="input input-bordered grow"
            placeholder="Abc"
            bind:value={userInfo.first_name}
          />
        </label>

        <label class="form-control">
          <div class="label">
            <span class="label-text">Last Name</span>
          </div>
          <input
            id="last_name"
            type="text"
            class="input input-bordered grow"
            placeholder="Xyz"
            bind:value={userInfo.last_name}
          />
        </label>

        <label class="form-control">
          <div class="label">
            <span class="label-text">Address line 1</span>
          </div>
          <input
            id="street_1"
            type="text"
            class="input input-bordered grow"
            placeholder="123 Main St"
            bind:value={userInfo.street_1}
          />
        </label>
        <label class="form-control">
          <div class="label">
            <span class="label-text">Address line 2</span>
          </div>
          <input
            id="street_2"
            type="text"
            class="input input-bordered grow"
            placeholder="Apt 4B"
            bind:value={userInfo.street_2}
          />
          <div class="label">
            <span class="label-text-alt">Optional</span>
          </div>
        </label>
        <label class="form-control">
          <div class="label">
            <span
              class="label-text
">City</span
            >
          </div>
          <input
            id="city"
            type="text"
            class="input input-bordered grow"
            placeholder="New York"
            bind:value={userInfo.city}
          />
        </label>
        <label class="form-control">
          <div class="label">
            <span class="label-text">State/Province</span>
          </div>
          <input
            id="state"
            type="text"
            class="input input-bordered grow"
            placeholder="NY"
            bind:value={userInfo.state}
          />
        </label>
        <label class="form-control">
          <div class="label">
            <span class="label-text">Zip/Postal Code</span>
          </div>
          <input
            id="zip_code"
            type="text"
            class="input input-bordered grow"
            placeholder="10001"
            bind:value={userInfo.zip_code}
          />
        </label>
        <label class="form-control">
          <div class="label">
            <span class="label-text">Country</span>
            <span class="label-text-alt">
              <a
                href="https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2"
                class="underline">ISO 3166-1 alpha-2</a
              >
            </span>
          </div>
          <input
            id="country"
            type="text"
            class="input input-bordered grow"
            placeholder="US"
            bind:value={userInfo.country}
          />
        </label>
      {/if}
      <div class="flex justify-center">
        <button type="submit" class="btn btn-primary mt-4" disabled={isLoading}>
          Login / Sign Up
        </button>
      </div>
    </form>
  {/if}
  <div class="text-center mt-4">
    <a href="/" class="text-sm text-blue-600 hover:text-blue-800"
      >← Back to Home</a
    >
  </div>
</div>
