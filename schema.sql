PRAGMA foreign_keys = ON;

drop table if exists event;
create table event (
  ID text primary key,
  name text not null,
  details text not null
);

drop table if exists trans;
create table trans (
  ID integer primary key autoincrement,
  eventID text,
  payerUID integer not null,
  recipUID integer not null,
  amount real,
  FOREIGN KEY(eventID) REFERENCES event(ID),
  FOREIGN KEY(payerUID) REFERENCES users(ID),
  FOREIGN KEY(recipUID) REFERENCES users(ID)
);

drop table if exists users;
create table users (
	ID integer primary key autoincrement,
	name text not null,
	phone text
);

drop table if exists participants;
create table participants (
	userID integer,
	eventID integer,
	PRIMARY KEY (userID, eventID),
	FOREIGN KEY (eventID) REFERENCES event(ID),
	FOREIGN KEY (userID) REFERENCES users(ID)
);


