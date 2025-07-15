-- create table for requests to be dumped after validation
CREATE TABLE discovery_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id TEXT NOT NULL,
    data TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
);
-- TODO: add table for device ID's and the related data from the JSON.
