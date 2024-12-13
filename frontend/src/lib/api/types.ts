export interface User {
    email: string;
}

export interface Event {
    name: string;
    description?: string;
}

export interface Project {
    name: string;
    readme: string;
    repo: string;
    description?: string;
    event: string | string[];
}

export interface Vote {
    event_id: string;
    projects: string[];
}
