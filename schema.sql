drop table if exists event;
create table event (
  ID integer primary key autoincrement,
  name text not null,
  details text not null,
);

drop table if exists trans;
create table trans (
  ID integer primary key autoincrement,
  eventID integer,
  payerUID integer not null,
  recipUID integer not null,
  amount real,
  FOREIGN KEY(eventID) REFERENCES event(ID),
  FOREIGN KEY(payerUID) REFERENCES user(ID),
  FOREIGN KEY(recipUID) REFERENCES user(ID)
);

drop table if exists user;
create table user (
	ID integer primary key autoincrement,
	firstname text not null,
	lastname text not null,
	email text,
	phone text
);

drop table if exists participants
create table participants (
	userID integer,
	eventID integer,
	PRIMARY KEY (userID, eventID),
	FOREIGN KEY (eventID) REFERENCES event(ID),
	FOREIGN KEY (userID) REFERENCES user(ID)
);


