export interface User {
    email: string;
}


export interface EventCreationPayload {
    name: string;
    description?: string;
}

export interface Event extends EventCreationPayload {
    id: string;
}

export interface OwnedEvent extends Event {
    attendees: string[];
   
    owner: string[];
    join_code: string;
}

export interface UserEvents {
    owned_events: OwnedEvent[];
    attending_events: EventCreationPayload[];
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