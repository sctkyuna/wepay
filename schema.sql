drop table if exists event;
create table event (
  eventID integer primary key autoincrement,
  name text not null,
  details text not null,
);

drop table if exists trans;
create table trans (
  transID integer autoincrement,
  eventID integer,
  payerUID integer not null,
  recipUID integer not null,
  amount real,
  PRIMARY KEY(transid, eventid),
  FOREIGN KEY(eventID) REFERENCES event(eventID)
);

