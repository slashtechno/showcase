import type { Project, Vote, Event } from "./types";
// @ts-ignore
import { env } from '$env/dynamic/public';
import { user } from '../stores';
import { derived } from "svelte/store";

const API_BASE: string = env.PUBLIC_API_URL 

export class ApiClient {
    private currentToken: string | null = null;
    private unsubscribe: () => void;

    constructor() {
        // Subscribe to user store changes
        this.unsubscribe = derived(user, $user => $user?.token)
            .subscribe(token => {
                this.currentToken = token ?? null;
                console.debug('Token updated in ApiClient:', this.currentToken);
            });
    }

    // Call this when ApiClient is no longer needed
    destroy() {
        // Clean up subscription to prevent memory leaks
        if (this.unsubscribe) {
            this.unsubscribe();
        }
    }

    private async fetch(endpoint: string, options: RequestInit = {}) {
        const url = `${API_BASE}${endpoint}`;
        
        if (this.currentToken) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${this.currentToken}`
            };
        }
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`API error: ${response.statusText}`);
        }
        return response;
    }


    // Auth endpoints
    async requestLogin(email: string) {
        const response = await this.fetch('/request-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        return response.json();
    }

    async verifyToken(token: string): Promise<{ access_token: string, token_type: string }> {
        const response = await this.fetch(`/verify?token=${token}`);
        user.set({ token: token, email: "" });
        return response.json();
    }

    // Events endpoints
    async getEvents() {
        const response = await this.fetch('/events/');
        return response.json();
    }

    async createEvent(event: Event) {
        const response = await this.fetch('/events/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(event)
        });
        return response.json();
    }

    async getAttendingEvents() {
        const response = await this.fetch('/events/attending');
        return response.json();
    }

    async attendEvent(joinCode: string) {
        const response = await this.fetch(`/events/attend?join_code=${joinCode}`, {
            method: 'POST'
        });
        return response.json();
    }

    async submitVote(vote: Vote) {
        const response = await this.fetch('/events/vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(vote)
        });
        return response.json();
    }

    async getLeaderboard(eventId: string) {
        const response = await this.fetch(`/events/${eventId}/leaderboard`);
        return response.json();
    }

    // Projects endpoints
    async getProjects() {
        const response = await this.fetch('/projects/');
        return response.json();
    }

    async createProject(project: Project) {
        const response = await this.fetch('/projects/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(project)
        });
        return response.json();
    }

    async getProject(projectId: string) {
        const response = await this.fetch(`/projects/${projectId}`);
        return response.json();
    }

    // This returns an object with the sole property of "email", on success
    async verifyAuth(token: string): Promise<{ email: string }> {
        const response = await this.fetch('/protected-route');
        return response.json();
    }
}

export const api = new ApiClient();
