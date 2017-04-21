create table _user (
  userId integer primary key autoincrement,
  email text not null,
  password text not null,
  firstName text primary key not null,
  lastName text primary key not null,
  profilePictureURL text not null
);