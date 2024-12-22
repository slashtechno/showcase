type User = {
    email: string;
    token: string;
    isAuthenticated: boolean;
};

export const user = $state<User>({
    email: "",
    token: "",
    isAuthenticated: false
});

export function signOut() {
    user.email = '';
    user.token = '';
    user.isAuthenticated = false;
    localStorage.removeItem('token');
}