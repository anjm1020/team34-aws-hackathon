CREATE TABLE member (
    id TEXT PRIMARY KEY,
    data JSONB,
    has_meeting BOOLEAN DEFAULT false
);

CREATE TABLE member_meeting (
    id SERIAL PRIMARY KEY,
    member_id TEXT,
    accept BOOLEAN
);

CREATE TABLE meeting (
    id SERIAL PRIMARY KEY,
    member_meeting_id1 INTEGER,
    member_meeting_id2 INTEGER,
    accept BOOLEAN,
    time TEXT
);