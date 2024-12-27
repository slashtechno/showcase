import { client } from "$lib/client/sdk.gen";
import { AuthService } from "$lib/client/sdk.gen";
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
    client.setConfig({
        headers: {
            Authorization: ''
        }
    });
    console.debug('User signed out, cleared user state, token in localStorage and headers');
}

export function validateToken(token: string): Promise<void> {

    return AuthService.protectedRouteProtectedRouteGet(
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    ).then((response) => {
        if (!response.data) {
            console.error('Invalid token', response);
            throw new Error('Invalid token');
        } 
        const data = response.data;
        user.email = data.email;
        user.token = token;
        user.isAuthenticated = true;
        client.setConfig({
            headers: {
                Authorization: `Bearer ${user.token}`
            }
        });
        console.debug('Token verified, set user state and headers');
    }).catch((err) => {
        console.log('Token is invalid', err);
        signOut();
    });

}
