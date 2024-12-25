import type { Project, Vote, EventCreationPayload, Event, UserEvents, OwnedEvent, ProjectCreationPayload, UserSignupPayload } from "./types";
// @ts-ignore
import { env } from '$env/dynamic/public';
import { user } from '../user.svelte';
import { error } from '@sveltejs/kit';


const API_BASE: string = env.PUBLIC_API_URL 

export class ApiClient {


    private async fetch(endpoint: string, options: RequestInit = {}) {
        const url = `${API_BASE}${endpoint}`;
        
        // if (user.isAuthenticated) {
        // Add Authorization header only if it's not already present
        if (!options.headers || !('Authorization' in options.headers)) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${user.token}`
            };
        }
        // }
        const response = await fetch(url, options);
        if (!response.ok) {
            // throw new Error(`API error: ${response.statusText}`);
            error(response.status, response.statusText);
        }
        return response;
    }


    // Auth endpoints
    async requestLogin(email: string): Promise<Object> {
        const response = await this.fetch('/request-login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        return response.json();
    }

    async verifyToken(token: string): Promise<{ access_token: string, token_type: string, email: string }> {
        const response = await this.fetch(`/verify?token=${token}`);
        return response.json();
    }

    async signupUser(user: UserSignupPayload): Promise<Object> {
        const response = await this.fetch('/users/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(user)
        });
        return response.json();
    }

    async userExists(email: string): Promise<{ exists: boolean }> {
        const response = await this.fetch(`/users/exists?email=${encodeURIComponent(email)}`);
        return response.json();
    }

    // At the moment this just returns whatever Airtable returns when it creates a new record
    async createEvent(event: EventCreationPayload): Promise<Object> {
        const response = await this.fetch('/events/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(event)
        });
        return response.json();
    }

    async getAttendingEvents(): Promise<UserEvents> {
        const response = await this.fetch('/events/');
        return response.json();
    }

    async getEvent(eventId: string): Promise<Event|OwnedEvent> {
        const response = await this.fetch(`/events/${eventId}`);
        return response.json();
    }


    async attendEvent(joinCode: string): Promise<Object> {
        const response = await this.fetch(`/events/attend?join_code=${joinCode}`, {
            method: 'POST'
        });
        return response.json();
    }

    async submitVote(vote: Vote): Promise<Object> {
        const response = await this.fetch('/events/vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(vote)
        });
        return response.json();
    }

    async getLeaderboard(eventId: string): Promise<[Project]> {
        const response = await this.fetch(`/events/${eventId}/leaderboard`);
        return response.json();
    }

    // Projects endpoints
    async getProjects(): Promise<Project[]> {
        const response = await this.fetch('/projects/');
        return response.json();
    }

    // Get event projects
    async getEventProjects(eventId: string): Promise<Project[]> {
        const response = await this.fetch(`/events/${eventId}/projects`);
        return response.json();
    } 

    async createProject(project: ProjectCreationPayload): Promise<Object> {
        const response = await this.fetch('/projects/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(project)
        });
        return response.json();
    }

    async getProject(projectId: string): Promise<Project> {
        const response = await this.fetch(`/projects/${projectId}`);
        return response.json();
    }

    // This returns an object with the sole property of "email", on success
    async verifyAuth(token: string): Promise<{ email: string }> {
        const response = await this.fetch('/protected-route', {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Test': `Bearer ${token}`
            }
        });
        return response.json();
    }
}

export const api = new ApiClient();
