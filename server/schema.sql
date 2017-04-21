create table server.user (
    userId INTEGER PRIMARY KEY autoincrement,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    firstName TEXT PRIMARY KEY NOT NULL,
    lastName TEXT PRIMARY KEY NOT NULL,
    profilePictureURL TEXT
);

create table server.activity (
    activityId INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
    maximumUsers INTEGER DEFAULT = 0
);

create table server.room (
    roomId INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
    maximumUsers INTEGER DEFAULT = 0
);

create table server.breakSeekerRequest (
    breakId INTEGER PRIMARY KEY,
    server.userId  INTEGER NOT NULL FOREIGN KEY,
    joined TEXT NOT NULL,
    status TEXT NOT NULL,
    activities BLOB NOT NULL
);

create table server.breakMatch (
    partners BLOB NOT NULL,
    server.activityId INTEGER NOT NULL FOREIGN KEY,
    server.roomId INTEGER NOT NULL FOREIGN KEY,
    _timestamp CURRENT_TIMESTAMP
);

create table server.apiResponse (
    code INTEGER NOT NULL,
    type TEXT NOT NULL,
    message TEXT NOT NULL
);