import { api } from "$lib/api/client.svelte";

type User = {
    email: string;
    token: string;
    isAuthenticated: boolean;
};

export const user: User = $state({
    email: "",
    token: "",
    isAuthenticated: false,
});

export function signOut() {
    user.email = '';
    user.token = '';
    user.isAuthenticated = false;
    localStorage.removeItem('token');
}

export function validateToken(token: string): Promise<void> {
    // console.debug("If you're seeing this on the server... that probably shouldn't happen. A wise message from user.svelte.ts");
    return api.verifyAuth(token).then((response) => {
        // Since it's $state we can do this. Assigning to user directly will not work as it's an import
        user.email = response.email;
        user.token = token;
        user.isAuthenticated = true;
        console.debug('Token verified, setting user in store', token);
    }).catch((err) => {
        console.log('Token is invalid', err);
        signOut();
    });
}
