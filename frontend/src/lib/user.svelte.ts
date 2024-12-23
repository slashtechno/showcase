type User = {
    email: string;
    token: string;
    isAuthenticated: boolean;
};

export const user: User = $state({
    email: "",
    token: "",
    isAuthenticated: false,
    set user(value: User) {
        Object.assign(user, value);
    }

    
});

export function signOut() {
    user.email = '';
    user.token = '';
    user.isAuthenticated = false;
    localStorage.removeItem('token');
}