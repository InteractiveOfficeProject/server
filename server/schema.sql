create table user (
    userId INTEGER PRIMARY KEY autoincrement,
    email TEXT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL
);

create table activity (
    activityId INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
    maximumUsers INTEGER DEFAULT NULL
);

create table room (
    roomId INTEGER PRIMARY KEY autoincrement,
    name TEXT NOT NULL,
    maximumUsers INTEGER DEFAULT NULL
);

create table break (
    breakId INTEGER PRIMARY KEY autoincrement,
    created DATETIME DEFAULT TIMESTAMP,
    status TEXT NOT NULL,
    user INTEGER,
    activity INTEGER,
    room INTEGER,
    FOREIGN KEY(user) REFERENCES user(userId),
    FOREIGN KEY(activity) REFERENCES activity(activityId),
    FOREIGN KEY(room) REFERENCES room(roomId)
);

create table participatesIn (
    user INTEGER,
    break INTEGER,
    FOREIGN KEY(user) REFERENCES user(userId),
    FOREIGN KEY(break) REFERENCES break(breakId)
);