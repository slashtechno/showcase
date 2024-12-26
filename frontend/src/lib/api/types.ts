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
    attending_events: Event[];
}

export interface ProjectCreationPayload {
    name: string;
    readme: string;
    repo: string;
    image_url: string;
    description?: string;
    event: string[];
}

export interface Project extends ProjectCreationPayload {
    id: string;
    points: number;
}

export interface Vote {
    event_id: string;
    projects: string[];
}

export interface UserSignupPayload {
    first_name: string;
    last_name: string;
    email: string;
    mailing_address: string;
}
